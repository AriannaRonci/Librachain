import solcx
from web3 import Web3
from solcx import compile_source
solcx.install_solc('0.6.0')

class OnChainController:

    def __init__(self):
        self.smart_contracts = "soliditycontracts"
        with open('soliditycontracts/OnChainManager.sol', 'r') as file:
            on_chain_source_code = file.read()
        compiled_contract = compile_source(on_chain_source_code, output_values=['abi', 'bin'])
        contract_id, contract_interface = compiled_contract.popitem()
        self.bytecode = contract_interface['bin']
        self.abi = contract_interface['abi']
        self.w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8548"))
        self.address = "0x254dffcd3277C0b1660F6d42EFbB754edaBAbC2B"
        self.counter = self.w3.eth.contract(address=self.address, abi=self.abi)



    def getDeployed(self, shardAddress):
        self.my_address = "0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1"
        result = self.counter.functions.getAddressList(shardAddress).call()
        print(result)

    def addToDictionary(self, shardAddress, contractAddress, myWallet):
        self.counter = self.w3.eth.contract(address=self.address, abi=self.abi)
        result = self.counter.functions.addToDictionary(shardAddress, contractAddress).transact({"from": myWallet})
        self.w3.eth.wait_for_transaction_receipt(result)
        print(result)



