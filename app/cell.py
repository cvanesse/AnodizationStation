# The base cell class holds:
#   A Bus
#   A CSVLog for logging
#   A Cycle
#       All Cycle management functions
from .cycle import Cycle
from .gpiocontrol import Bus
from .logger import CSVLog
from .pisense import CurrentSensor


class Cell:

    cell_cycle = Cycle()

    def __init__(self, buspins, logfile, sensoraddress):
        self.cell_bus = Bus([buspins])
        self.cell_log = CSVLog(logfile, ['Time', 'Current'])
        self.cell_current_sensor = CurrentSensor(sensoraddress)

    def set_cycle(self, newcycle):
        self.cell_cycle = newcycle

    def run_cycle(self, numcycles):
        for i in range(numcycles):
            for j in range(self.cell_cycle.allcyclecommands):
                self.cell_cycle.pop()
