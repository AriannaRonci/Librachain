from eth_utils import decode_hex
from web3 import Web3

from cli.command_line_interface import CommandLineInterface
from controllers.on_chain_controller import OnChainController
from controllers.shards_controller import ShardsController
from session.session import Session
from eth_keys import keys

if __name__ == "__main__":

    session_obj = Session()

    cli = CommandLineInterface(session_obj)
    while True:
        cli.print_menu()




