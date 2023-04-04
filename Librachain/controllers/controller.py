from dal.user_repository import UserRepository
from session.session import Session
from models.user import User

class Controller:
    
    def __init__(self, session):
        self.user_repo = UserRepository()
        self.session = session

    def login(self, username, password):
        if self.check_number_attempts() and self.user_repo.check_password(username, password):
            user = self.user_repo.get_user_by_username(username)
            self.session.setUser(user.getUsername())
            return 0
        elif self.check_number_attempts():
            self.session.incrementLoginAttempts()
            return -1
        else:
            return -2

    def check_number_attempts(self):
        if self.session.attempts < 5:
            return True
        else:
            return False



    def register(self, username, password, public_key, private_key):
        if self.user_repo.register_user(username, password, public_key, private_key):
            user = self.user_repo.get_user_by_username(username)
            self.session.setUser(user)
            return True
        else:
            return False

    def decrypt_private_key(self, encrypted_private_key, password):
        return self.user_repo.decrypt_private_key(encrypted_private_key, password)
