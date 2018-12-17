# The Pin class holds a state and an ID
class BasePin:

    pinState = False
    pinID = -1

    def __init__(self, pid):
        self.pinState = False
        self.pinID = pid

    def setstate(self, flag):
        self.pinState = flag
        self.update()

    def getstate(self):
        return self.pinState

    def getid(self):
        return self.pinID

    def update(self):
        pass
