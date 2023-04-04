from cli.command_line_interface import CommandLineInterface
from controllers.on_chain_controller import OnChainController
from session.session import Session

if __name__ == "__main__":
    my_wallet = "0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1"
    session_obj = Session()
    cli = CommandLineInterface(session_obj)
    while True:
        cli.print_menu()
