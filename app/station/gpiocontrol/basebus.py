# The bus class holds an array of pins and can handles updating the state of them all
class BaseBus:
    busPins = []

    def __init__(self, pinSet):
        self.busPins = pinSet

    def setstate(self, state):
        for pid in range(len(self.busPins)):
            self.busPins[pid].setstate(state[pid])

        self.update()

    def getstate(self):
        state = []
        for pin in self.busPins:
            state.append(pin.getstate())

        return state

    def update(self):
        pass
