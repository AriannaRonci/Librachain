from web3 import Web3

from controllers.on_chain_controller import OnChainController


class ShardsController:

    def __init__(self, w3):
        self.w3 = w3

    def deploy_smart_contract(self, smart_contract_path, wallet):
        with open(smart_contract_path, 'r') as file:
            smart_contract_code = file.read()
        #compiled_contract = compile_source(smart_contract_code, output_values=['abi', 'bin'])
        #contract_id, contract_interface = compiled_contract.popitem()
        #abi = contract_interface['abi']


    def by_abi(self, smart_contract_address, abi):
        invoke_onchain = OnChainController()
        result = invoke_onchain.get_shard(smart_contract_address)
        if result:
            contract = self.w3.eth.contract(address=smart_contract_address, abi=abi)
            print(contract.all_functions())
