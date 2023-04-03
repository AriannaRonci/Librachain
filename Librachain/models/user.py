class User:
    def __init__(self, id, username, password_hash, public_key, private_key):
        self.__id = id
        self.__username = username
        self.__password_hash = password_hash
        self.__public_key = public_key
        self.__private_key = private_key

    def getUsername(self):
        return self.__username

    def getPasswordHash(self):
        return self.__password_hash
        
    def getPublicKey(self):
        return self.__public_key

    def getPrivateKey(self):
        return self.__private_key
