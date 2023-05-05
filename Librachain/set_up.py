import logging
import solcx
from web3 import Web3, HTTPProvider
from solcx import compile_standard, compile_source

solcx.install_solc('0.6.0')

with open('set_parameters.txt', 'r') as f:
    for line in f:
        line_to_read = '- Number of shards:'
        if line.startswith(line_to_read):
            num_of_shards = line.split(line_to_read, 1)[1]

base_shard = 'http://localhost:'
base_address = 8546
base_name = 'shard'
shard_names = []
shard_addresses = []
shards = []
for i in range(1, int(num_of_shards)+1):
    shard_addresses.append(base_shard + str(base_address))
    base_address = base_address+1
    shard_names.append(base_name + str(i))
    shards.append(Web3(HTTPProvider(shard_addresses[i-1])))

# Set up the web3 provider
#shard1 = Web3(HTTPProvider('http://localhost:8545'))
#shard2 = Web3(HTTPProvider('http://localhost:8546'))
#shard3 = Web3(HTTPProvider('http://localhost:8547'))


#shards = [shard1, shard2, shard3]

# Set up the contract and account information
contract_name = 'OnChain'
accounts = []
for i in range(1, int(num_of_shards)+1):
    accounts.append(shards[i-1].eth.accounts[0])

#account1 = shard1.eth.accounts[0]
#account2 = shard2.eth.accounts[0]
#account3 = shard3.eth.accounts[0]

#accounts = [account1, account2, account3]

contract1 = 'soliditycontracts/Ballot.sol'
contract2 = 'soliditycontracts/Storage.sol'
contract3 = 'soliditycontracts/ERC20.sol'
contract4 = 'soliditycontracts/Owner.sol'

contracts = [contract2, contract4]
with open('soliditycontracts/contract_address.txt', 'r') as f:
    onchain_address = f.readline().strip('\n')
with open('soliditycontracts/OnChainManager.sol', 'r') as file:
    on_chain_source_code = file.read()

compiled_onchain = compile_source(on_chain_source_code, output_values=['abi', 'bin'])
onchain_id, onchain_interface = compiled_onchain.popitem()
onchain_abi = onchain_interface['abi']
onchain_w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
onchain_address = onchain_address
on_chain = onchain_w3.eth.contract(address=onchain_address, abi=onchain_abi)

for i in range(0, 2):
    with open(contracts[i]) as f:
        contracts_code = f.read()
    compiled_contract = compile_source(contracts_code, output_values=['abi', 'bin'])
    contract_id, contract_interface = compiled_contract.popitem()
    contract_abi = contract_interface['abi']
    contract_bytecode = contract_interface['bin']

    for j in range(0, int(num_of_shards)-1):
        MyContract = shards[j].eth.contract(abi=contract_abi, bytecode=contract_bytecode)
        tx_hash = MyContract.constructor().transact({'from': accounts[j]})
        receipt = shards[j].eth.wait_for_transaction_receipt(tx_hash)
        logging.basicConfig(filename='soliditycontracts/log.txt',
                            filemode='w',
                            level=logging.INFO, format='')
        a = "account: " + accounts[j] + "; "
        c = "contract: " + contracts[i] + "; "
        r = "contract address: " + receipt['contractAddress']
        splitted_r = r.split(": ", 1)[1]
        on_chain.functions.addToDictionary(shard_names[j], splitted_r).transact({'from': accounts[j]})
        shard_name = shard_names[j]
        logging.info('%s %s %s %s', a, c, shard_name, r)


print(dict(receipt))
