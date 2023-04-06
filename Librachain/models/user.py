class User:
  
    def __init__(self, id, username, password_hash, public_key, private_key):
        self.__id = id
        self.__username = username
        self.__password_hash = password_hash
        self.__public_key = public_key
        self.__private_key = private_key

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
