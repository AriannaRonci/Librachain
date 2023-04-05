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

    # invoke_onchain.get_balance("http://127.0.0.1:8548")
    # print("add to dictionary")
    # print(invoke_onchain.add_to_dictionary("http://127.0.0.1:8545", "0x254dffcd3277C0b1660F6d42EFbB754edaBAbC2B", my_wallet))
    print("get address list")
    print(invoke_onchain.get_address_list("http://127.0.0.1:8545"))
    print("invoke get shard")
    print(invoke_onchain.get_shard("0x254dffcd3277C0b1660F6d42EFbB754edaBAbC2B"))
    shards_controller = ShardsController(Web3(Web3.HTTPProvider("http://127.0.0.1:8545")))
    print("shards controller abi")
    print(shards_controller.by_abi("0xCfEB869F69431e42cdB54A4F4f105C19C080A601", [
        {
            "inputs": [],
            "name": "retrieve",
            "outputs": [
                {
                    "internalType": "uint256",
                    "name": "",
                    "type": "uint256"
                }
            ],
            "stateMutability": "view",
            "type": "function"
        },
        {
            "inputs": [
                {
                    "internalType": "uint256",
                    "name": "num",
                    "type": "uint256"
                }
            ],
            "name": "store",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function"
        }
    ]))
    # session_obj = Session()
    # cli = CommandLineInterface(session_obj)
    # while True:
    #    cli.print_menu()



