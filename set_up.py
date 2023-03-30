import logging
import solcx
from web3 import Web3, HTTPProvider
from solcx import compile_standard, compile_source
solcx.install_solc('0.6.0')
import json

# Set up the web3 provider
shard1 = Web3(HTTPProvider('http://localhost:8545'))
shard2 = Web3(HTTPProvider('http://localhost:8546'))
shard3 = Web3(HTTPProvider('http://localhost:8547'))

shards = [shard1, shard2, shard3]

# Set up the contract and account information
contract_name = 'OnChain'
account1 = shard1.eth.accounts[0]
account2 = shard2.eth.accounts[0]
account3 = shard3.eth.accounts[0]

accounts = [account1, account2, account3]

contract1 = 'Librachain/soliditycontracts/Ballot.sol'
contract2 = 'Librachain/soliditycontracts/Storage.sol'
contract3 = 'Librachain/soliditycontracts/ERC20.sol'
contract4 = 'Librachain/soliditycontracts/Owner.sol'

contracts = [contract1, contract2, contract3, contract4]

for i in range (1,5):
	with open(contracts[i]) as f:
        	contracts_code = f.read()
	compiled_contract = compile_source(contracts_code, output_values=['abi','bin'])
	contract_id, contract_interface = compiled_contract.popitem()
	contract_abi = contract_interface['abi']
	contract_bytecode = contract_interface['bin']
	for j in range (1,4):
        	MyContract = shards[j].eth.contract(abi=contract_abi,bytecode=contract_bytecode)
		tx_hash = MyContract.constructor().transact({'from': accounts[j]})
		receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
		logging.basicConfig(filename='Librachain/soliditycontracts/contract_address.txt', level=logging.DEBUG, format='')
		logging.info('%s %s %s', accounts[j], contracts [i], receipt['contractAddress'])

print(dict(receipt))
