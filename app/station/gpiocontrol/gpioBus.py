from .gpioPin import GPIOPin
from .basebus import BaseBus


# The GPIOBus is for use with an RPi
class GPIOBus(BaseBus):

    def __init__(self, pids):
        pins = []
        for pid in pids:
            pins.append(GPIOPin(pid))

        BaseBus.__init__(self, pinSet=pins)

    def update(self):
        pass


