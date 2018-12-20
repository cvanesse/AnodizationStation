# The base cell class holds:
#   A Bus
#   A CSVLog for logging
#   A Cycle
#       All Cycle management functions
from .cycle import Cycle
from .gpiocontrol import Bus
from .logger import CSVLog
from .pisense import CurrentSensor
import time


class Cell:

    cycle = Cycle()
    bus = []

    def __init__(self, buspins, logfile, sensoraddress):
        self.bus = Bus([buspins])
        self.log = CSVLog(logfile, ['Time [s]', 'Current [mA]'])
        self.current_sensor = CurrentSensor(sensoraddress)

    def set_cycle(self, newcycle):
        self.cycle = newcycle

    def run_cycle(self, numcycles):
        for i in range(numcycles):
            for j in range(len(self.cycle.allcyclecommands)):
                self.cycle.pop()

    # Cell.log handles logging the current time and all the sensors of the cell
    def log(self):
        self.log.write([time.clock(), self.current_sensor.read()])

    # Cell.time_delay does a time delay for the given amount of seconds while still logging
    def time_delay(self, seconds):
        start = time.clock()
        current = start
        while current - start < seconds:
            self.log.write([current, self.current_sensor.read()])
            current = time.clock()

    # Cell.charge_delay does a charge delay for the given amount of seconds while still logging
    def charge_delay(self, charge):
        curcharge = 0
        then = time.clock()
        while curcharge < charge:
            current = self.current_sensor.read()
            now = time.clock()
            curcharge += current*(now - then)
            self.log.write([now, current])
            then = now

    def set_bus_state(self, sid):
        if sid == 1:
            self.bus.setstate([1, 1, 1, 1])
        else:
            self.bus.setstate([0, 0, 0, 0])
