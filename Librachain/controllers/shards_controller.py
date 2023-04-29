import solcx
import web3.exceptions
from web3 import Web3, HTTPProvider
from web3.exceptions import ContractLogicError, InvalidAddress


from controllers.on_chain_controller import OnChainController
from solcx import compile_source

from dal.user_repository import UserRepository

solcx.install_solc('0.6.0')


class ShardsController:
    """
    ShardsController manages the interaction between shards, user and On-Chain-Controller
    """

    def __init__(self, session):
        self.__shards = ['http://localhost:8545', 'http://localhost:8546', 'http://localhost:8547']
        self.session = session
        self.user_repo = UserRepository()

    def get_shards(self):
        return self.__shards

    def create_contract(self, smart_contract_path):
        """
        This class creates a contract object based on source code and chooses the w3 provider
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

    def deploy_smart_contract(self, smart_contract_path, gas_limit, gas_price, wallet, password):
        """
        Deployes a smart contract
        :param private_key: private key of user
        :param smart_contract_path: path of the source code of the smart contract
        :param gas_limit: gas limit of the smart contract to deploy
        :param gas_price: gas price of the smart contract to deploy
        :param wallet: wallet of the user
        :return:
            - contract address if the try does not fail
            - name of the choosed shard
        """
        try:
            my_contract, w3 = self.create_contract(smart_contract_path)
            tx = my_contract.constructor().build_transaction({
                                                     'gasPrice': int(gas_price),
                                                     'gas': int(gas_limit),
                                                     'from': wallet,
                                                     'nonce': w3.eth.get_transaction_count(wallet)
                                                     })
            #print(w3.eth.estimateGas(tx))
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
            invoke_onchain = OnChainController()
            shard = self.balance_load().provider.endpoint_uri
            invoke_onchain.add_to_dictionary(shard, receipt['contractAddress'], wallet)
            return receipt['contractAddress'], self.balance_load().provider.endpoint_uri
        except ContractLogicError as cle:
            raise cle
        except Exception as ex:
            raise ex

    def estimate(self, smart_contract_path, gas_limit, gas_price):
        """
        Estimates the gas used for a certain transaction
        :param smart_contract_path: path of the source code of the smart contract
        :param gas_limit: gas limit of the transaction
        :param gas_price: gas price of the transaction
        :return: the amount of gas estimated if the try does not fail
        """
        my_contract, w3 = self.create_contract(smart_contract_path)
        try:
            tx = my_contract.constructor().build_transaction({
                'gasPrice': gas_price,
                'gas': gas_limit
            })
            gas = w3.eth.estimate_gas(tx)
            return gas
        except ContractLogicError:
            return -1
        except:
            return -2

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
            invoke_onchain = OnChainController()
            valid_address = (invoke_onchain.is_valid_address(shard, smart_contract_address))
            if valid_address:
                w3 = Web3(Web3.HTTPProvider(shard))
                contract = w3.eth.contract(address=smart_contract_address, abi=abi)
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
        except Exception as ex:
            raise ex

    def call_function(self, web3, function_name, i, attributes, contract, my_wallet, password):
        """
        calls or transacts the function chosen by the user
        :param password:
        :param web3:
        :param function_name: name of the chosen function
        :param i: index of the chosen function
        :param attributes: chosen attributes by the user
        :param contract: built contract by souce code and address
        :param my_wallet: wallet of the user
        :return: return of the called function
        """
        try:
            calling_function = getattr(contract.functions, function_name)
            if contract.abi[i]['stateMutability'] == 'view':
                return calling_function(*attributes).call()
            else:
                tx = calling_function(*attributes).build_transaction({
                                                     'from': my_wallet,
                                                     'nonce': web3.eth.get_transaction_count(my_wallet)
                })
                private_key = self.user_repo.decrypt_private_key(self.session.get_user().get_private_key(), password)
                signed_tx = web3.eth.account.sign_transaction(tx, private_key=private_key)
                return web3.eth.send_raw_transaction(signed_tx.rawTransaction)

        except InvalidAddress as ia:
            raise ia
        except web3.exceptions.ValidationError as ve:
            raise ve
        except Exception as ex:
            raise ex

    def balance_load(self):
        """
        Balances the load of the blockchain
        :return: calculated provider to make next transaction is the
                 try does not fail
        """
        try:
            shard1 = Web3(HTTPProvider('http://localhost:8545'))
            shard2 = Web3(HTTPProvider('http://localhost:8546'))
            shard3 = Web3(HTTPProvider('http://localhost:8547'))
            shards_providers = [shard1, shard2, shard3]
            shards_name = ['shard1', 'shard2', 'shard3']
            shards = {
                shards_name[0]: shard1.eth.block_number,
                shards_name[1]: shard2.eth.block_number,
                shards_name[2]: shard3.eth.block_number
            }
            for i in range(0, len(shards)):
                if i == 0:
                    chosen_shard = shards_providers[i]
                elif shards[shards_name[i]] < shards[shards_name[i - 1]]:
                    chosen_shard = shards_providers[i]
            return chosen_shard
        except Exception as ex:
            raise ex
