from cli.command_line_interface import CommandLineInterface
from controllers.shards_controller import ShardsController
from session.session import Session
from solidity_parser import parser


if __name__ == "__main__":
    session_obj = Session()
    cli = CommandLineInterface(session_obj)
    while True:
        cli.print_menu()
