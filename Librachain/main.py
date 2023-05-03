from colorama import Fore, Style
from web3 import Web3

from cli.command_line_interface import CommandLineInterface
from controllers.on_chain_controller import OnChainController
from controllers.shards_controller import ShardsController
from session.session import Session

if __name__ == "__main__":

    #shard_controller = ShardsController()
    """shard_controller.deploy_smart_contract("/Users/chiaragobbi/Desktop/Università/magistrale/primo anno/primo semestre/"
                                           "software security and block chain/progetto/swsb-project/Librachain/"
                                           "soliditycontracts/OnChainManager.sol", 200000000, 200000000,
                                           '0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1',
                                           '0x4f3edf983ac636a65a842ce7c78d9aa706d3b113bce9c46f30d7d21715b23b1d')
    

    #session_obj = Session()
    #shard_controller = ShardsController(session_obj)
    #cli_functions, contract, function_names, w3 = shard_controller.smart_contract_methods_by_sourcecode('http://localhost:8546',
    #                                                                                                    '0xD833215cBcc3f914bD1C9ece3EE7BF8B14f841bb',
    #                                     "/Users/chiaragobbi/Desktop/Università/magistrale/primo anno/primo semestre/"
    #                                     "software security and block chain/progetto/swsb-project/Librachain/"
    #                                     "soliditycontracts/OnChainManager.sol")

    #estimated = shard_controller.estimate_methodcall(w3, 'addToDictionary', ['ciao', '0xC89Ce4735882C9F0f0FE26686c53074E09B0D550'], contract,
    #                                                 202020202, 220202020, '0xD833215cBcc3f914bD1C9ece3EE7BF8B14f841bb')
    #print(estimated)
    #attributes = ['ciao', '0xC89Ce4735882C9F0f0FE26686c53074E09B0D550']

    #calling_function = getattr(my_contract.functions, 'addToDictionary')
    #tx = calling_function(*attributes).build_transaction({
    #            'gasPrice': 2000000,
    #            'gas': 20000000,
    #            'to': '0xD833215cBcc3f914bD1C9ece3EE7BF8B14f841bb'
    #        })
    #web3 = Web3(Web3.HTTPProvider('http://localhost:8545'))
    #gasprice = web3.eth.generate_gas_price()
    #print(w3.eth.estimate_gas(tx))
"""

    session_obj = Session()
    cli = CommandLineInterface(session_obj)
    while True:
        cli.print_menu()
