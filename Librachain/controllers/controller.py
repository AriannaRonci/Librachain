from dal.user_repository import UserRepository
from models.smart_contract import SmartContract
from session.session import Session
from models.user import User


class Controller:
    """Interface between user interfaces and the model. Handles authentication too.

    Attributes:
        user_repo: UserRepository object (See class documentation)
        session: Session object (See class documentation)
        __max_login_attempts: Integer, maximum number of allowed 
            consecutive failed login attempts
        __locking_time: Integer, seconds the user should be locked after exceeding 
            the failed login attempts limit
    """

    def __init__(self, session: Session):
        """Initializes the class.

        Args:
            session: shared Session object
        """
        self.user_repo = UserRepository()
        self.session = session
        self.__max_login_attempts = 5
        self.__locking_time = 300

    def login(self, username: str, password: str, public_key: str, private_key: str):
        """Handles login logic. 

        Calls the user_repository methods to check if supplied credentials are 
        correct. Checks that the maximum number of consecutive login attempts is 
        not exceeded. If a user exceeds the limit, other attempts can't be 
        performed for __locking_time seconds. Session attributed are set 
        accordingly to the result.

        Args:
            - username: username string supplied in the login attempt
            - password: password string supplied in the login attempt

        Returns:
            An integer that identifies the outcome:
                 0: correct credentials
                -1: wrong credentials
                -2: number of login attempts exceeded
        """
        if self.check_number_attempts() and self.user_repo.check_password(username, password):
            user = self.user_repo.get_user_by_username(username)
            self.session.set_user(user)
            return 0
        elif self.check_number_attempts():
            self.session.increment_attempts()
            if self.session.get_attempts() == self.__max_login_attempts:
                self.session.set_exceeded_attempts_timeout(self.__locking_time)
            return -1
        else:
            return -2

    def check_password(self, username: str, password: str):
        """Checks if the supplied credentials are present in the databse

        Args:
            - username: username string supplied in the login attempt
            - password: password string supplied in the login attempt

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

        if self.session.get_attempts() < self.__max_login_attempts:
            return True
        else:
            return False

    def register(self, username: str, password: str, public_key: str, private_key: str):
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

        FIX:
            -missing register check
        """
        registering_result = self.user_repo.register_user(username, password,
                                                          public_key, private_key)
        if registering_result == 0:
            user = self.user_repo.get_user_by_username(username)
            self.session.set_user(user)

        return registering_result

    def decrypt_private_key(self, encrypted_private_key: str, password: str):
        """Decrypts the supplied encrypted private key.
        
        Decrypts the supplied encrypted private key using the supplied password.
        Decryption done using the decrypt_private_key method in UserRepository,
        as decryption logic is handled there.

        Args:
            encrypted_private_key: string containing user's encrypted private key
            password: string containing the password used to perform decrypton on 
                encrypted_private_key

        Returns:
            A string containing the decrypted private key
        """
        return self.user_repo.decrypt_private_key(encrypted_private_key, password)

    def insert_smart_contract(self, name: str, address: str, shard: int, user: User):
        """Insert smart_contract in database and model.

        WORK IN PROGRESS
        """
        smart_contract = SmartContract(name, address, shard, user.get_id())
        result = self.user_repo.insert_deployed_smart_contract(smart_contract)
        if result == 0:
            try:
                smart_contract = self.user_repo.get_smart_contract_by_address(address, shard)
                self.session.get_user().add_smart_contract(smart_contract)
            except:
                return -1
        return result

    def delete_smart_contract(self, smart_contract: SmartContract):
        """Deletes smart contract in database and model.

        WORK IN PROGRESS
        """
        try:
            self.user_repo.delete_deployed_smart_contract(smart_contract)
            self.session.get_user().delete_smart_contract(smart_contract.get_id())
            return 0
        except:
            return -1

    def change_password(self, username, new_password, old_password):
        if self.user_repo.check_password(username, old_password):
            self.user_repo.change_password(username, new_password, old_password)

    def check_password_obsolete(self, username):
        return self.user_repo.is_password_obsolete(username)
