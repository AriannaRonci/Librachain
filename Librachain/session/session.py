# import uuid
import time
from models.user import User

class Session:
    """Used to share information on the current session between objects.
    Attributes:
        __user: logged in User object
        __attempts: Integer, current consecutive failed login attempts
        __exceededTimestamp: Integer, timestamp for login unlock
    """

    def __init__(self):
        self.__user = None
        # self.__id = str(uuid.uuid4())
        self.__attempts = 0
        self.__exceeded_timestamp = 0

    def get_user(self):
        """ __user getter.
        
        Returns:
         A User object or None if no user is logged in.
        """
        return self.__user

    def set_user(self, user):
        """__user setter"""
        self.__user = user

    def get_attempts(self):
        """__attempts getter"""
        return self.__attempts

    def increment_attempts(self):
        self.__attempts += 1

    def reset_attempts(self):
        self.__attempts = 0

    def set_exceeded_attempts_timeout(self, lock_time: int):
        """Sets __exceeded_timestamp to lock_time seconds from when called"""
        self.__exceeded_timestamp = time.time() + lock_time

    def get_time_left_for_unlock(self):
        """Returns seconds left till __exceededTimestmap"""
        return self.__exceeded_timestamp - time.time()
