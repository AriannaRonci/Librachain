import solcx
import web3.exceptions
from web3 import Web3, HTTPProvider
from web3.exceptions import ContractLogicError, InvalidAddress
from web3.logs import DISCARD

from controllers.on_chain_controller import OnChainController
from solcx import compile_source

from dal.user_repository import UserRepository

solcx.install_solc('0.6.0')


class ShardsController:
    """
    ShardsController manages the interaction between shards, user and On-Chain-Controller
    """

    def __init__(self, session, num_shards):
        self.__num_shards = num_shards
        self.__shard_names, self.__shards = self.define_shards()
        self.session = session
        self.user_repo = UserRepository()
        self.invoke_onchain = OnChainController()

    def get_shards(self):
        """
        Allows to get a list of shard addresses
        :return: a list of shard addresses
        """
        return self.__shards

    def define_shards(self):
        """
        Creates a list of shard names and shard addresses
        :return:
            - a list of shard names
            - a list of shard addresses
        """
        base_shard = 'http://localhost:'
        base_address = 8545
        base_name = 'shard'
        shard_names = []
        shards = []
        for i in range(1, self.__num_shards+1):
            base_address = base_address+1
            shards.append(base_shard + str(base_address))
            shard_names.append(base_name + str(i))
        return shard_names, shards

    def create_contract(self, smart_contract_path):
        """
        Creates a contract object based on source code and chooses the w3 provider
        considering the load on the blockchain
        :param smart_contract_path: path of the source code of the smart contract
        :return: built contract and w3 provider
        """
        try:
            with open(smart_contract_path, 'r') as file:
                smart_contract_code = file.read()
            compiled_contract = compile_source(smart_contract_code, output_values=['abi', 'bin'])
            contract_id, contract_interface = compiled_contract.popitem()
            contract_abi = contract_interface['abi']
            contract_bytecode = contract_interface['bin']
            w3 = self.balance_load()
            if w3 != 'Error Occurred':
                my_contract = w3.eth.contract(abi=contract_abi,
                                              bytecode=contract_bytecode)
                return my_contract, w3
        except Exception:
            raise Exception

    def deploy_smart_contract(self, smart_contract_path, attr, gas_limit, gas_price, wallet, password):
        """
        Deployes a smart contract
        :param smart_contract_path: path of the source code of the smart contract
        :param gas_limit: gas limit of the smart contract to deploy
        :param gas_price: gas price of the smart contract to deploy
        :param wallet: wallet of the user
        :param password: password of the user
        :param attr: parameters in constructor
        :return:
            - contract address if the try does not fail
            - address of the chose shard
        """
        try:
            my_contract, w3 = self.create_contract(smart_contract_path)
            if attr == []:
                tx = my_contract.constructor().build_transaction({
                    'gasPrice': int(gas_price),
                    'gas': int(gas_limit),
                    'from': wallet,
                    'nonce': w3.eth.get_transaction_count(wallet)
                })
            else:
                tx = my_contract.constructor(*attr).build_transaction({
                    'gasPrice': int(gas_price),
                    'gas': int(gas_limit),
                    'from': wallet,
                    'nonce': w3.eth.get_transaction_count(wallet)
                })
            private_key = self.user_repo.decrypt_private_key(self.session.get_user().get_private_key(), password)
            signed_tx = w3.eth.account.sign_transaction(tx, private_key=private_key)
            raw_tx = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            """
            tx_hash = my_contract.constructor().transact({'gasPrice': gas_price,
                                                          'gasLimit': gas_limit,
                                                          'from': wallet})
            receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
            """
            receipt = w3.eth.wait_for_transaction_receipt(raw_tx)
            shard = w3.provider.endpoint_uri
            self.invoke_onchain.add_to_dictionary(int(shard.split('http://localhost:')[1]), receipt['contractAddress'], wallet, private_key)
            return receipt['contractAddress'], shard
        except ContractLogicError as cle:
            raise cle
        except Exception as ex:
            raise ex

    def estimate(self, smart_contract_path, attr, gas_limit, gas_price):
        """
        Estimates the gas used for a certain transaction
        :param smart_contract_path: path of the source code of the smart contract
        :param attr: parameters of constructor
        :param gas_limit: gas limit of the transaction
        :param gas_price: gas price of the transaction
        :return: the amount of gas estimated if the try does not fail
        """
        try:
            my_contract, w3 = self.create_contract(smart_contract_path)
            if attr == []:
                tx = my_contract.constructor().build_transaction({
                    'gasPrice': gas_price,
                    'gas': gas_limit
                })
                gas = w3.eth.estimate_gas(tx)
                return gas
            else:
                tx = my_contract.constructor(*attr).build_transaction({
                    'gasPrice': gas_price,
                    'gas': gas_limit
                })
                gas = w3.eth.estimate_gas(tx)
                return gas
        except ContractLogicError:
            return -1
        except Exception as ex:
            #print(ex)
            return -2

    def check_parameters(self, smart_contract_path):
        try:
            my_contract, w3 = self.create_contract(smart_contract_path)
            parameter_types = []
            for i in my_contract.abi:
                if i['type'] == 'constructor':
                    if len(i['inputs'][0]) > 0:
                        constructor = i['inputs']
                        for j in constructor:
                            parameter_types.append(j['type'])
                        return 1, w3, parameter_types
                else:
                    return -1, w3, parameter_types
        except Exception as ex:
            raise ex

    def smart_contract_methods_by_sourcecode(self, shard, smart_contract_address, path_source_code):
        """
        Retrieves smart contract methods
        :param shard: shard name
        :param smart_contract_address: address of the deployed smart contract
        :param path_source_code: path of the source code of the smart contract
        :return: if try does not fail
            - cli_functions: array of functions with params
            - contract: contract object built
            - function_names: array of the name of the function
            - w3 provider
        """
        try:
            with open(path_source_code, 'r') as file:
                source_code = file.read()
            compiled_contract = compile_source(source_code, output_values=['abi', 'bin'])
            contract_id, contract_interface = compiled_contract.popitem()
            abi = contract_interface['abi']
            bytecode = contract_interface['bin']
            valid_address = self.invoke_onchain.is_valid_address(int(shard.split('http://localhost:')[1]), smart_contract_address)
            if valid_address:
                w3 = Web3(Web3.HTTPProvider(shard))
                contract = w3.eth.contract(address=smart_contract_address, abi=abi, bytecode=bytecode)
                functions = contract.all_functions()
                cli_functions = []
                for i in range(0, len(functions)):
                    function = str(functions[i]).replace('<Function', '').replace('>', '')
                    cli_functions.append(function)
                function_names = []
                sep = '('
                for i in range(0, len(cli_functions)):
                    stripped = cli_functions[i].split(sep, 1)[0].replace(' ', '')
                    function_names.append(stripped)
                return cli_functions, contract, function_names, w3
            else:
                return -1
        except Exception as ex:
            raise ex

    def call_function(self, w3, function_name, attributes, contract, my_wallet, password, gas_price, gas_limit, view):
        """
        calls or transacts the function chosen by the user
        :param w3: provider to use to call the function
        :param function_name: name of the chosen function
        :param attributes: chosen attributes by the user
        :param contract: built contract by souce code and address
        :param my_wallet: wallet of the user
        :param password: password of the user
        :param gas_limit: gas limit of the transaction
        :param gas_price: gas price of the transaction
        :param view: is true if the function to call is view
        :return: if the try does not fail:
            - receipt of the transaction
            - list of events generated from calling the contract
            - list of event names

        """
        try:
            calling_function = getattr(contract.functions, function_name)
            if view == 1:
                return calling_function(*attributes).call()
            else:
                tx = calling_function(*attributes).build_transaction({
                                                     'gasPrice': int(gas_price),
                                                     'gas': int(gas_limit),
                                                     'from': my_wallet,
                                                     'nonce': w3.eth.get_transaction_count(my_wallet),
                                                     #'address': contract_address
                })
                private_key = self.user_repo.decrypt_private_key(self.session.get_user().get_private_key(), password)
                signed_tx = w3.eth.account.sign_transaction(tx, private_key=private_key)
                sent_tx = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
                receipt = w3.eth.wait_for_transaction_receipt(sent_tx)

                event = []
                event_names = []

                for i in range(0, len(contract.events._events)):
                    event_name = str(contract.events._events[i]['name'])
                    event_names.append(event_name)
                    calling_event = getattr(contract.events, event_name)()
                    event.append(calling_event.process_receipt(receipt, errors=DISCARD)[0]['args'])

                return receipt, event, event_names
        except InvalidAddress as ia:
            raise ia
        except web3.exceptions.ValidationError as ve:
            raise ve
        except ContractLogicError as cle:
            raise cle
        except Exception as ex:
            raise ex

    def estimate_methodcall(self, w3, function_name, attributes, contract, gas_price, gas_limit, contract_address):
        """
        estimate the cost of calling a function
        :param w3: provider to use to call the function
        :param function_name: name of the chosen function
        :param attributes: chosen attributes by the user
        :param contract: built contract by souce code and address
        :param gas_limit: gas limit of the transaction
        :param gas_price: gas price of the transaction
        :param contract_address: address of the contract to call
        :return: if the try does not fail:
            - the gas estimated for calling the smart contract
        """
        try:
            calling_function = getattr(contract.functions, function_name)
            tx = calling_function(*attributes).build_transaction({
                'gasPrice': gas_price,
                'gas': gas_limit,
                'address': contract_address
            })
            gas = w3.eth.estimate_gas(tx)
            return gas
        except Exception as ex:
            return -1

    def balance_load(self):
        """
        Balances the load of the blockchain
        :return: calculated provider to which deploy the contract if the try does not fail
        """
        shards_providers = []
        shards = {}
        try:
            for i in range(1, self.__num_shards+1):
                shards_providers.append(Web3(HTTPProvider(self.__shards[i-1])))
                shards.update({self.__shard_names[i-1]: shards_providers[i-1].eth.block_number})
            for i in range(0, len(shards)):
                if i == 0:
                    chosen_shard = shards_providers[i]
                elif shards[self.__shard_names[i]] < shards[self.__shard_names[i - 1]]:
                    chosen_shard = shards_providers[i]
            return chosen_shard
        except Exception as ex:
            raise ex
