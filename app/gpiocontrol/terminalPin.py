from .basepin import BasePin


# The Terminal Test Pin is for testing on non-RPi PCs
class TerminalTestPin(BasePin):

    def __init__(self, id):
        BasePin.__init__(self, id)

    def update(self):
        pass

