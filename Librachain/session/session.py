#import uuid

class Session:
    def __init__(self):
        self.user = None
        #self.id = str(uuid.uuid4())
        self.attempts = 0

    def getUser(self):
        return self.user

    def setUser(self,user):
        self.user = user

    def getAttempts(self):
        return self.attempts

    def incrementLoginAttemps(self):
        self.attempts += 1
