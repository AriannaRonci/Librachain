from cli.command_line_interface import CommandLineInterface
from controllers.controller import Controller
from controllers.on_chain_controller import OnChainController
from session.session import Session

if __name__ == "__main__":
    myWallet = "0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1"
    invoke_onchain = OnChainController()
    invoke_onchain.getBalance("http://127.0.0.1:8548")
    invoke_onchain.getAddressList("http://127.0.0.1:8548")
    invoke_onchain.addToDictionary("http://127.0.0.1:8548", "0x254dffcd3277C0b1660F6d42EFbB754edaBAbC2B", myWallet)
    session_obj = Session()
    cli = CommandLineInterface(session_obj)
    while (True):
        cli.print_menu()
