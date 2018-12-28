from .terminalPin import TerminalTestPin
from .basebus import BaseBus


# The TerminalBus is for testing on non-RPi PCs
class TerminalBus(BaseBus):
    def __init__(self, pids):
        pins = []
        for pid in pids:
            pins.append(TerminalTestPin(pid))

        BaseBus.__init__(self, pinSet=pins)

    def update(self):
        output = ''
        for pin in self.busPins:
            output = output + '|' + str(pin.getid()) + ':' + str(pin.getstate())
        print('-' * len(output))
        print(output)
