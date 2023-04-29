from colorama import Fore, Style

from cli.command_line_interface import CommandLineInterface
from controllers.shards_controller import ShardsController
from session.session import Session

if __name__ == "__main__":
    """
    shard_controller = ShardsController()
    shard_controller.deploy_smart_contract("/Users/chiaragobbi/Desktop/Università/magistrale/primo anno/primo semestre/"
                                           "software security and block chain/progetto/swsb-project/Librachain/"
                                           "soliditycontracts/OnChainManager.sol", 200000000, 200000000,
                                           '0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1',
                                           '0x4f3edf983ac636a65a842ce7c78d9aa706d3b113bce9c46f30d7d21715b23b1d')

"""

    session_obj = Session()
    cli = CommandLineInterface(session_obj)
    while True:
        cli.print_menu()

