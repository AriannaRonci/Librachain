from web3 import Web3

from controllers.on_chain_controller import OnChainController


class ShardsController:

    def __init__(self, w3):
        self.w3 = w3

    def by_abi(self, smart_contract_address, abi, wallet):
        invoke_onchain = OnChainController()
        result = invoke_onchain.get_shard(smart_contract_address)
        if result:
            contract = self.w3.eth.contract(address=smart_contract_address, abi=abi)
            print(contract.all_functions())






