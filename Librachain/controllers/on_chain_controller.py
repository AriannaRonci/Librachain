import solcx
from web3 import Web3
from solcx import compile_source

solcx.install_solc('0.6.0')


class OnChainController:

    def __init__(self):
        with open('soliditycontracts/contract_address.txt', 'r') as f:
            contract_address = f.readline().strip('\n')
        with open('soliditycontracts/OnChainManager.sol', 'r') as file:
            on_chain_source_code = file.read()

        compiled_contract = compile_source(on_chain_source_code, output_values=['abi', 'bin'])
        contract_id, contract_interface = compiled_contract.popitem()
        self.abi = contract_interface['abi']
        self.w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8548"))
        self.address = contract_address
        # print(contract_address)
        self.on_chain = self.w3.eth.contract(address=self.address, abi=self.abi)

    def get_address_list(self, shard_address):
        result = self.on_chain.functions.getAddressList(shard_address).call()
        return result
        # print(result)

    def add_to_dictionary(self, shard_address, contract_address, my_wallet):
        result = self.on_chain.functions.addToDictionary(shard_address, contract_address).transact({"from": my_wallet})
        self.w3.eth.wait_for_transaction_receipt(result)
        # print(result)

    def get_balance(self, shard_address):
        result = self.on_chain.functions.getBalance(shard_address).call()
        return result
        # print(result)

    def get_shard(self, shard_address):
        result = self.on_chain.functions.getShard(shard_address).call()
        return result
        # print(result)
