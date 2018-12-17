#This is the wrapper for the ina219 current sensor
from ina219 import INA219
from sensor import Sensor


class CurrentSensor(Sensor):

    SHUNT = 0.1
    MAX_EXPECTED_AMPS = 1

    def __init__(self, i2c):
        self.ina = INA219(self.SHUNT, self.MAX_EXPECTED_AMPS)
        self.ina.configure(self.ina.RANGE_16V)
        self.ina.sleep()
        Sensor.__init__(self)

    def read(self):
        self.ina.wake()
        if not self.ina.current_overflow():
            current = self.ina.current()
        else:
            current = self.MAX_EXPECTED_AMPS
        self.ina.sleep()
        return current
