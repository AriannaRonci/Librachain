<<<<<<< HEAD
from cli.CommandLineInterface import CommandLineInterface
from controller.Controller import Controller
=======
import controller
from controller.OnChainController import OnChainController
>>>>>>> main

if __name__ == "__main__":

    #cli = CommandLineInterface()
    #while (True):
    #    cli.print_menu()
    myWallet = "0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1"
    invoke_onchain = OnChainController()
    invoke_onchain.addToDictionary("http://127.0.0.1:8548", "0x254dffcd3277C0b1660F6d42EFbB754edaBAbC2B", myWallet)
    invoke_onchain.getDeployed("http://127.0.0.1:8548")
