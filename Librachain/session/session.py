#import uuid
import time

class Session:
    def __init__(self):
        self.__user = None
        #self.__id = str(uuid.uuid4())
        self.__attempts = 0
        self.__exceededTimestamp = 0

    def getUser(self):
        return self.user

    def setUser(self,user):
        self.user = user

    def getAttempts(self):
        return self.attempts

    def incrementLoginAttemps(self):
        self.attempts += 1

    def resetAttempts(self):
        self.attempts = 0

    def setExceededAttemptsTimeout(self):
        self.__exceededTimestamp = time.time() + 300
        
    def getTimeLeftForUnlock():
        return self.__exceededTimestamp-time.time()
