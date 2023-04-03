import logging
import solcx
from web3 import Web3, HTTPProvider
from solcx import compile_standard, compile_source
solcx.install_solc('0.6.0')

# Set up the web3 provider
web3 = Web3(HTTPProvider('http://localhost:8548'))

# Set up the contract and account information
contract_name = 'OnChain'
account = web3.eth.accounts[0]
contract_file = 'soliditycontracts/OnChainManager.sol'
with open(contract_file) as f:
	on_chain_source_code = f.read()
#contract_abi = contract_json['abi']
#contract_bytecode = contract_json['bytecode']

compiled_contract = compile_source(on_chain_source_code, output_values=['abi', 'bin'])
contract_id, contract_interface = compiled_contract.popitem()
contract_abi = contract_interface['abi']
contract_bytecode = contract_interface['bin']

# Deploy the contract
contract_address = '0x2612Af3A521c2df9EAF28422Ca335b04AdF3ac66'

MyContract = web3.eth.contract(abi=contract_abi, 
bytecode=contract_bytecode)
tx_hash = MyContract.constructor().transact({'from': account})
receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

logging.basicConfig(filename='soliditycontracts/contract_address.txt', level=logging.DEBUG, format='')
logging.info(receipt['contractAddress'])

print(dict(receipt))

