#The digipinsensor reads a digital pin onf the Raspberry Pi
try:
    from RPi import GPIO
except RuntimeError:
    print('Cannot use digipinsensor.')

from .sensor import Sensor


class DigiPinSensor(Sensor):

    pinID = -1

    def __init__(self, pid):
        self.pinID = pid
        GPIO.setup(pid, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        Sensor.__init__(self)

    def read(self):
        return GPIO.input(self.pinID)
