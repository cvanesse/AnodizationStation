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
from multiprocessing import Process


# The Cell should be created within the same subprocess that runs Cell.run_cycle
class Cell:

    # These will eventually be set during initialization of the program
    ina_address = 0x40
    tag_names = ['Time [s]', 'Current [mA]']

    def __init__(self, buspins, logfile):
        self.bus = Bus(buspins)
        self.log = CSVLog(logfile, self.tag_names)
        self.current_sensor = CurrentSensor(self.ina_address)

    # This sets the cycle a new cycle object
    def set_cycle(self, cycle):
        self.cycle = cycle

    # To be run on a child process
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
        now = start
        while now - start < seconds:
            self.log.write([now, self.current_sensor.read()])
            now = time.clock()

    # Cell.charge_delay does a charge delay for the given amount of seconds while still logging
    def charge_delay(self, total_charge):
        charge = 0
        then = time.clock()
        then_current = self.current_sensor.read()

        while charge < total_charge:

            now = time.clock()
            now_current = self.current_sensor.read()

            charge += (now_current + then_current) * (now - then) / 2
            self.log.write([now, now_current])

            then = now
            then_current = now_current

    # Cell.set_bus_state sets the bus to the configured state
    def set_bus_state(self, sid):
        if sid == 1:
            self.bus.setstate([1, 1, 1, 1])
        else:
            self.bus.setstate([0, 0, 0, 0])
