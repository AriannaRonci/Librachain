import solcx
import web3.exceptions
from web3 import Web3, HTTPProvider
from web3.exceptions import ContractLogicError, InvalidAddress

from controllers.on_chain_controller import OnChainController
from solcx import compile_source

solcx.install_solc('0.6.0')

"""

"""
class ShardsController:
    def __init__(self):
        pass

    def create_contract(self, smart_contract_path):
        try:
            with open(smart_contract_path, 'r') as file:
                smart_contract_code = file.read()
            compiled_contract = compile_source(smart_contract_code, output_values=['abi', 'bin'])
            contract_id, contract_interface = compiled_contract.popitem()
            contract_abi = contract_interface['abi']
            contract_bytecode = contract_interface['bin']
            w3 = self.balance_load()
            my_contract = w3.eth.contract(abi=contract_abi,
                                          bytecode=contract_bytecode)
            return my_contract, w3
        except FileNotFoundError:
            print("File not found")
        except:
            print("Compiling error")

    def deploy_smart_contract(self, smart_contract_path, gas_limit, gas_price, wallet):
        my_contract, w3 = self.create_contract(smart_contract_path)
        try:
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
        except:
            return -2

    def estimate(self, smart_contract_path, gas_limit, gas_price, wallet):
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
            print("Error Occurred")


    def smart_contract_methods_by_sourcecode(self,smart_contract_address, path_source_code):
        try:
            with open(path_source_code, 'r') as file:
                source_code = file.read()
            compiled_contract = compile_source(source_code, output_values=['abi', 'bin'])
            contract_id, contract_interface = compiled_contract.popitem()
            abi = contract_interface['abi']
            invoke_onchain = OnChainController()
            w3 = Web3(HTTPProvider(invoke_onchain.get_shard(smart_contract_address)))
            if w3 != 'contract not deployed':
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
        except FileNotFoundError:
            print("File not found")
        except:
            print("Error occurred")

    def call_function(self, function_name, attributes, contract):
        try:
            calling_function = getattr(contract.functions, function_name)
            return calling_function(*attributes).call()
        except InvalidAddress:
            print("The specified address is not valid.")
        except web3.exceptions.ValidationError:
            print('Wrong number of inputs')
        except:
            print("Error Occurred")

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


