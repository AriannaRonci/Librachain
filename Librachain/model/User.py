class User:
    def __init__(self, id, username, password_hash, public_key)
        self.id = id
        self.__username = username
        self.__password_hash = password_hash
        self.__public_key = public_key
        self.__private_key = private_key

    def getUsername():
        return self.__username

    def getPasswordHash():
        return self.__password_hash
        
    def getPublicKey():
        return self.__public_key

    def getPrivateKey():
        return self.__private_key
