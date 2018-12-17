from .basepin import BasePin
from RPi import GPIO


# The GPIOPin holds a modified update definition which actually updates the output pin
class GPIOPin(BasePin):

    def __init__(self, gpioid):
        GPIO.setup(gpioid, GPIO.OUT, initial=GPIO.LOW)
        BasePin.__init__(self, gpioid)

    def update(self):
        GPIO.output(self.pinID, self.pinState)
