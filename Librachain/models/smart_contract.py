class SmartContract:

    def __init__(self, id: int, name, address, user_id:int):
        self.__id = id
        self.__name = name
        self.__address = address
        self.__user_id = user_id

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_address(self):
        return self.__address

    def get_user_id(self):
        return self.__user_id
