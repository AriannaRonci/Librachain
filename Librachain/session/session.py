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
        self.__exceededTimestamp = 0

    def getUser(self):
        """ __user getter.
        
        Returns:
         A User object or None if no user is logged in.
        """
        return self.__user

    def setUser(self, user: User):
        """__user setter"""
        self.__user = user

    def getAttempts(self):
        """__attempts getter"""
        return self.__attempts

    def incrementLoginAttempts(self):
        self.__attempts += 1

    def resetAttempts(self):
        self.__attempts = 0

    def setExceededAttemptsTimeout(self, lock_time: int):
        """Sets __exceededTimestamp to lock_time seconds from when called"""
        self.__exceededTimestamp = time.time() + lock_time

    def getTimeLeftForUnlock(self):
        """Returns seconds left till __exceededTimestmap"""
        return self.__exceededTimestamp - time.time()
