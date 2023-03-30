#import uuid

class Session:
    def __init__(self, user):
        self.user = user
        #self.id = str(uuid.uuid4())
        self.attempts = 0

    def getUser():
        return self.user

    def setUser(user):
        self.user = user

    def getAttempts():
        return self.attempts

    def incrementLoginAttemps():
        self.attempts += 1
