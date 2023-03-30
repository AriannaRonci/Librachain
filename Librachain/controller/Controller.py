#from dal.user_repository import UserRepository

class Controller:
    
    #__init__(self, session):
        #self.user_repo = UserRepository()

    def login(self, username, password, public_key, private_key):
        #Mettiamo tutta la logica dei tentativi qui?
        #if ...
        #   session.setUser(user)
        #   return True
        #else
        #    return False
        #    session.incrementLoginAttempts()
        pass

    def register(self, username, password, public_key, private_key):
        #self.user_repo.register(username, password, public_key, private_key)
        #user = self.user_repo.get_user_by_username(username)
        #session.setUser(user)
        pass

    def decrypt_private_key(self, encrypted_private_key, password):
        return self.user_repo.decrypt_private_key(encrypted_private_key, password)

