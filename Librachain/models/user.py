from models.smart_contract import SmartContract

class User:
  
    def __init__(self, id: int, username:str, password_hash:str, public_key:str, private_key:str, deployed_smart_contracts=[]):
        self.__id = id
        self.__username = username
        self.__password_hash = password_hash
        self.__public_key = public_key
        self.__private_key = private_key
        self.__deployed_smart_contracts = deployed_smart_contracts

    def get_id(self):
        return self.__id
    
    def get_username(self):
        return self.__username

    def get_password_hash(self):
        return self.__password_hash
        
    def get_public_key(self):
        return self.__public_key

    def get_private_key(self):
        return self.__private_key

    def get_smart_contracts(self):
        return self.__deployed_smart_contracts

    def add_smart_contract(self, smart_contract : SmartContract):
        self.__deployed_smart_contracts.append(smart_contract)
    
    def delete_smart_contract(self, sc_id: int):
        """Deletes smart contract corresponding to supplied id.

        Args:
            sc_id: Integer, smart contract to delete id
        """
        self.__deployed_smart_contracts = list(filter(
                lambda sc: sc.getId() != sc_id,
                self.__deployed_smart_contracts))
