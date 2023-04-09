import solcx
import web3.exceptions
from web3 import Web3, HTTPProvider
from web3.exceptions import ContractLogicError, InvalidAddress

from controllers.on_chain_controller import OnChainController
from solcx import compile_source

solcx.install_solc('0.6.0')


class ShardsController:
    """
    ShardsController manages the interaction between shards, user and On-Chain-Controller
    """

    def __init__(self):
        self.__shards = ['http://localhost:8545', 'http://localhost:8546', 'http://localhost:8547']

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
        except FileNotFoundError:
            raise FileNotFoundError
        except Exception:
            raise Exception

    def deploy_smart_contract(self, smart_contract_path, gas_limit, gas_price, wallet):
        """
        Deployes a smart contract
        :param smart_contract_path: path of the source code of the smart contract
        :param gas_limit: gas limit of the smart contract to deploy
        :param gas_price: gas price of the smart contract to deploy
        :param wallet: wallet of the user
        :return: contract address if the try does not fail
        """
        try:
            my_contract, w3 = self.create_contract(smart_contract_path)
            tx_hash = my_contract.constructor().transact({'gasPrice': gas_price,
                                                          'gasLimit': gas_limit,
                                                          'from': wallet})
            receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
            invoke_onchain = OnChainController()
            invoke_onchain.add_to_dictionary(self.balance_load().provider.endpoint_uri, receipt['contractAddress'],
                                             wallet)
            return receipt['contractAddress']
        except ContractLogicError:
            return -1
        #except FileNotFoundError:
        #    return -3
        except Exception:
            return -2

    def estimate(self, smart_contract_path, gas_limit, gas_price, wallet):
        """
        Estimates the gas used for a certain transaction
        :param smart_contract_path: path of the source code of the smart contract
        :param gas_limit: gas limit of the transaction
        :param gas_price: gas price of the transaction
        :param wallet: wallet of the user
        :return: the amount of gas estimated if the try does not fail
        """
        my_contract, w3 = self.create_contract(smart_contract_path)
        try:
            tx = my_contract.constructor().build_transaction({
                'gasPrice': gas_price,
                'gasLimit': gas_limit,
                'from': wallet
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
        :param smart_contract_address: address of the deployed smart contract
        :param path_source_code: path of the source code of the smart contract
        :return: if try does not fail
            - cli_functions: array of functions with params
            - contract: contract object built
            - function_names: array of the name of the functions
        """
        try:
            with open(path_source_code, 'r') as file:
                source_code = file.read()
        except:
            raise Exception
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
            return cli_functions, contract, function_names

    def call_function(self, function_name, i, attributes, contract, my_wallet):
        """
        Calls a Smart Contract method
        :param function_name: name of the function to call
        :param attributes: attributes of the function to call
        :param contract: contract object built by source code and address
        :return: boolean true if the call() method is successful
        """
        try:
            calling_function = getattr(contract.functions, function_name)
            if contract.abi[i]['stateMutability'] == 'view':
                return calling_function(*attributes).call()
            else:
                return calling_function(*attributes).transact({'from': my_wallet})
        except InvalidAddress:
            return -1
        except web3.exceptions.ValidationError as e:
            print(e)
            return -2
        except Exception as e:
            print(e)
            return -3

    # not used
    def by_abi(self, smart_contract_address, abi):
        invoke_onchain = OnChainController()
        w3 = Web3(HTTPProvider(invoke_onchain.get_shard(smart_contract_address)))
        if w3 != 'contract not deployed':
            contract = w3.eth.contract(address=smart_contract_address, abi=abi)
            functions = contract.all_functions()
            cli_functions = []
            for i in range(0, len(functions)):
                function = str(functions[i]).replace('<Function', '').replace('>', '')
                cli_functions.append(function)
            return cli_functions, contract, functions

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
        except:
            print("Error Occurred")
