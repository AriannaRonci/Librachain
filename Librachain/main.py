from cli.command_line_interface import CommandLineInterface
from controllers.on_chain_controller import OnChainController
from session.session import Session

if __name__ == "__main__":
    my_wallet = "0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1"
    invoke_onchain = OnChainController()
    invoke_onchain.get_balance("http://127.0.0.1:8548")
    invoke_onchain.get_address_list("http://127.0.0.1:8548")
    invoke_onchain.add_to_dictionary("http://127.0.0.1:8548", "0x254dffcd3277C0b1660F6d42EFbB754edaBAbC2B", my_wallet)
    session_obj = Session()
    cli = CommandLineInterface(session_obj)
    while True:
        cli.print_menu()
