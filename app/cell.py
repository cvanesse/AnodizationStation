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

    cell_cycle = Cycle()

    def __init__(self, buspins, logfile, sensoraddress):
        self.cell_bus = Bus([buspins])
        self.cell_log = CSVLog(logfile, ['Time [s]', 'Current [mA]'])
        self.cell_current_sensor = CurrentSensor(sensoraddress)

    def set_cycle(self, newcycle):
        self.cell_cycle = newcycle

    def run_cycle(self, numcycles):
        for i in range(numcycles):
            for j in range(len(self.cell_cycle.allcyclecommands)):
                self.cell_cycle.pop()

    # Cell.log handles logging the current time and all the sensors of the cell
    def log(self):
        self.cell_log.write([time.clock(), self.cell_current_sensor.read()])

    # Cell.time_delay does a time delay for the given amount of seconds while still logging
    def time_delay(self, seconds):
        start = time.clock()
        current = start
        while current - start < seconds:
            self.cell_log.write([current, self.cell_current_sensor.read()])
            current = time.clock()

    # Cell.charge_delay does a charge delay for the given amount of seconds while still logging
    def charge_delay(self, charge):
        curcharge = 0
        then = time.clock()
        while curcharge < charge:
            current = self.cell_current_sensor.read()
            now = time.clock()
            curcharge += current*(now - then)
            self.cell_log.write([now, current])
            then = now

    def set_bus_state(self, sid):
        if sid == 1:
            self.cell_bus.setstate([1, 1, 1, 1])
        else:
            self.cell_bus.setstate([0, 0, 0, 0])
