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
        #self.bytecode = contract_interface['bin']
        self.abi = contract_interface['abi']
        self.w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8548"))
        self.address = contract_address
        print(contract_address)
        self.counter = self.w3.eth.contract(address=self.address, abi=self.abi)



    def getDeployed(self, shardAddress):
        result = self.counter.functions.getAddressList(shardAddress).call()
        print(result)

    def addToDictionary(self, shardAddress, contractAddress, myWallet):
        result = self.counter.functions.addToDictionary(shardAddress, contractAddress).transact({"from": myWallet})
        self.w3.eth.wait_for_transaction_receipt(result)
        print(result)

    def getBalance(self, shardAddress):
        result = self.counter.functions.getBalance(shardAddress).call()
        print(result)


