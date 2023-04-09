class SmartContract:

    def __init__(self, name, address, shard, user_id:int, id: int = 0):
        self.__id = id
        self.__name = name
        self.__address = address
        self.__shard = shard
        self.__user_id = user_id

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_address(self):
        return self.__address

    def get_shard(self):
        return self.__shard

    def get_user_id(self):
        return self.__user_id
