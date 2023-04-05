# import uuid
import time

class Session:
    def __init__(self):
        self.__user = None
        # self.__id = str(uuid.uuid4())
        self.__attempts = 0
        self.__exceededTimestamp = 0

    def getUser(self):
        return self.__user

    def setUser(self, user):
        self.user = user

    def getAttempts(self):
        return self.__attempts

    def incrementLoginAttempts(self):
        self.__attempts += 1

    def resetAttempts(self):
        self.__attempts = 0

    def setExceededAttemptsTimeout(self, lock_time):
        self.__exceededTimestamp = time.time() + lock_time

    def getTimeLeftForUnlock(self):
        return self.__exceededTimestamp - time.time()
