from dal.user_repository import UserRepository
from session.session import Session

class Controller:
    
    def __init__(self, session):
        self.user_repo = UserRepository()
        self.session = session

    def login(self, username, password, public_key, private_key):
        if session.attempts < 5 and self.user_repo.check_password(username, password):
            session.setUser(user)
            return True
        elif session.attempts < 5:
            session.incrementLoginAttempts()
            return False
        else:
            return False

    def register(self, username, password, public_key, private_key):
        if self.user_repo.register(username, password, public_key, private_key):
            user = self.user_repo.get_user_by_username(username)
            session.setUser(user)
            return True
        else:
            return False

    def decrypt_private_key(self, encrypted_private_key, password):
        return self.user_repo.decrypt_private_key(encrypted_private_key, password)
