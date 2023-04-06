import solcx
from web3 import Web3, HTTPProvider

from controllers.on_chain_controller import OnChainController
from solcx import compile_source

solcx.install_solc('0.6.0')

class ShardsController:
    def __init__(self):
        pass

    def deploy_smart_contract(self, smart_contract_path, gas_limit, gas_price, wallet):
        with open(smart_contract_path, 'r') as file:
            smart_contract_code = file.read()
        compiled_contract = compile_source(smart_contract_code, output_values=['abi', 'bin'])
        contract_id, contract_interface = compiled_contract.popitem()
        contract_abi = contract_interface['abi']
        contract_bytecode = contract_interface['bin']
        w3 = self.balance_load()
        my_contract = w3.eth.contract(abi=contract_abi,
                                          bytecode=contract_bytecode)
        tx_hash = my_contract.constructor().transact({'gasPrice': gas_price,
                                                      'gasLimit': gas_limit,
                                                      'from': wallet})
        #print("fee=")
        #print(w3.eth.max_priority_fee())
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        print(receipt['contractAddress'])
        print(dict(receipt))
        invoke_onchain = OnChainController()
        invoke_onchain.add_to_dictionary(self.balance_load().provider.endpoint_uri, receipt['contractAddress'], wallet)

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
            print(cli_functions)
            return cli_functions, contract, functions

    def balance_load(self):
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
        print(chosen_shard)
        return chosen_shard

    def call_function(self, contract_function, contract):
        pass









