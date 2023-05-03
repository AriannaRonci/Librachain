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
        self.on_chain = self.w3.eth.contract(address=self.address, abi=self.abi)

    def get_address_list(self, shard_address):
        result = self.on_chain.functions.getAddressList(shard_address).call()
        return result

    def add_to_dictionary(self, shard_address, contract_address, my_wallet, private_key):
        try:
            tx = self.on_chain.functions.addToDictionary(shard_address, contract_address).build_transaction(
                {'from': my_wallet,
                 'gasPrice': self.w3.eth.gas_price,
                 'nonce': self.w3.eth.get_transaction_count(my_wallet)
                 }
            )
            signed_tx = self.w3.eth.account.sign_transaction(tx, private_key=private_key)
            sent_tx = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            receipt = self.w3.eth.wait_for_transaction_receipt(sent_tx)
            added_to_dict = self.on_chain.events.AddedToDict().process_receipt(receipt)[0]['args']
            return added_to_dict['result']
        except Exception as ex:
            raise ex

    def get_balance(self, shard_address):
        result = self.on_chain.functions.getBalance(shard_address).call()
        return result

    def is_valid_address(self, shard, shard_address):
        try:
            result = self.on_chain.functions.isValidAddress(shard, shard_address).call()
            return result
        except Exception as ex:
            raise ex
