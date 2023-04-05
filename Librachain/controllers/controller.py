from dal.user_repository import UserRepository
from session.session import Session
from models.user import User


class Controller:
    """Interface between user interfaces and the model. Handles authentication too.

    Attributes:
        user_repo: UserRepository object (See class documentation)
        session: Session object (See class documentation)
        __max_login_attempts: Integer representing the maximum number of allowed consecutive failed login attempts
        __locking_time: Integer representing the seconds the user should be locked after exceeding the failed login attempts limit
    """    

    def __init__(self, session):
        """Initializes the class.

        Args:
            session: shared Session object
        """
        self.user_repo = UserRepository()
        self.session = session
        self.__max_login_attempts = 5
        self.__locking_time = 300

    def login(self, username, password):
        """Handles login logic. 

        Calls the user_repository methods to check if the supplied credentials are correct.
        Checks that the maximum number of consecutive login attempts is not exceeded.
        If a user exceeds the limit, other attempts can't be performed for __locking_time seconds.
        Session attributed are set accrodingly to the result.

        Args:
            - username: string containing the username supplied in the login attempt
            - password: string containing the password supplied in the login attempt

        Returns:
            An integer that identifies the outcome:
                 0: correct credentials
                -1: wrong credentials
                -2: number of login attempts exceeded
        """
        if self.check_number_attempts() and self.user_repo.check_password(username, password):
            user = self.user_repo.get_user_by_username(username)
            self.session.setUser(user.getUsername())
            return 0
        elif self.check_number_attempts():
            self.session.incrementLoginAttempts()
            if self.session.getAttempts() == self.__max_login_attempts:
                self.session.setExceededAttemptsTimeout(self.__locking_time)
            return -1
        else:
            return -2

    def check_password(self, username, password):
        """Checks if the supplied credentials are present in the databse

        Args:
            - username: string containing the username supplied in the login attempt
            - password: string containing the password supplied in the login attempt

        Returns:
            An boolean that identifies the outcome:
                True: correct credentials
                False: wrong credentials
        """
        return self.user_repo.check_password(username, password)

    def check_number_attempts(self):
        """Checks if attempts exceed the maximum limit.
        
        Returns:
            A boolean:
                - True: the attempts do not exceed the attempts limit
                - False: the attempts exceed the attempts limit
        """

        if self.session.getAttempts() < self.__max_login_attempts:
            return True
        else:
            return False

    def register(self, username, password, public_key, private_key):
        """Handles user registration logic.

        Args:
            username: string containing registering user's username
            password: string containing registering user's password
            public_key: string containing registering user's public_key
            private_key: string containing registering user's private_key

        Returns:
            An integer that identifies the outcome:
                 0: user registered correctly
                -1: username already present in the database
                -2: unknown database error
        """
        if self.user_repo.register_user(username, password, public_key, private_key):
            user = self.user_repo.get_user_by_username(username)
            self.session.setUser(user)
            return True
        else:
            return False

    def decrypt_private_key(self, encrypted_private_key, password):
        """Decrypts the supplied encrypted private key.
        
        Decrypts the supplied encrypted private key using the supplied password.
        Decryption done using the decrypt_private_key method in UserRepository, as decryption logic is handled there.

        Args:
            encrypted_private_key: string containing user's encrypted private key
            password: string containing the password used to perform decrypton on encrypted_private_key

        Returns:
            A string containing the decrypted private key
        """
        return self.user_repo.decrypt_private_key(encrypted_private_key, password)
