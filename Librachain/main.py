from cli.command_line_interface import CommandLineInterface
from controllers.shards_controller import ShardsController
from session.session import Session

if __name__ == "__main__":

    session_obj = Session()

    shards_controller = ShardsController()
    #address = shards_controller.deploy_smart_contract("/Users/chiaragobbi/Desktop/Università/magistrale/primo anno/primo semestre/software security and block chain/progetto/swsb-project/Librachain/soliditycontracts/OnChainManager.sol", "20000000", "200000000", "0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1")
    #print(address)
    provider = "http://localhost:8545"
    address = "0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1"

    function_strings, contract, function_names = shards_controller.smart_contract_methods_by_sourcecode("0x9561C133DD8580860B6b7E504bC5Aa500f0f06a7","/Users/chiaragobbi/Desktop/Università/magistrale/primo anno/primo semestre/software security and block chain/progetto/swsb-project/Librachain/soliditycontracts/OnChainManager.sol")
    print(function_names)
    print(function_strings)

    command = shards_controller.call_function("addToDictionary", ["ciao", 0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1])
    exec(command)

    #command = "contract_built.functions."+str(function_names[0])+"('ciao','0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1').call()"
    #command = "contract_built.functions."+function_names[0]+"('http://localhost:8545','0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1')"
    #exec(command)
    #contract_built.functions.functions[0].call()

    #address = shards_controller.deploy_smart_contract("/Users/chiaragobbi/Desktop/Università/magistrale/primo anno/primo semestre/software security and block chain/progetto/swsb-project/Librachain/soliditycontracts/OnChainManager.sol","2000000", "20000000", "0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1")


	#cli = CommandLineInterface(session_obj)
		#while True:
		#    cli.print_menu()
