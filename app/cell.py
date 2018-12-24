from .gpiocontrol import Bus, Pin
from .logger import CSVLog
from .pisense import CurrentSensor
import time
from threading import Thread


# The Cell should be created within the same subprocess that runs Cell.run_cycle
class Cell:

    # These will eventually be set during initialization of the program
    ina_address = 0x40
    tag_names = ['Time [s]', 'Current [mA]']

    # We read sensors and log data on a separate thread from the control thread
    sensor_thread = []
    keep_sensing = False
    current = []

    # We need a way to communicate with the CellHandler, and a state variable for various signals
    cell_pipe = []
    die = []

    def __init__(self, runningpin, buspins, logfile, cellpipe):
        self.bus = Bus(buspins)
        self.running_pin = Pin(runningpin)
        self.log = CSVLog(logfile, self.tag_names)
        self.current_sensor = CurrentSensor(self.ina_address)
        self.cell_pipe = cellpipe
        self.cell_pipe.send(-1)
        self.die = False

    # This sets the cycle a new cycle object
    def set_cycle(self, cycle):
        self.cycle = cycle

    # To be run on a child process
    def run_cycle(self, numcycles):
        self.set_bus_state('S')
        self.running_pin.setstate(1)

        sensor_thread = Thread(target=self.sensor_loop)
        self.keep_sensing = True
        sensor_thread.start()

        for i in range(numcycles):
            self.cycle.run()
            self.cell_pipe.send(i/numcycles)

        self.keep_sensing = False
        sensor_thread.join()

        self.running_pin.setstate(0)

    # The loop run on the designated sensing thread
    def sensor_loop(self):
        while self.keep_sensing:
            now = time.clock()
            self.current = self.current_sensor.read()
            self.log.write([now, self.current])
            if self.cell_pipe.poll():
                self.die = self.cell_pipe.recv()

    # Cell.log handles logging the current time and all the sensors of the cell
    def log(self):
        self.log.write([time.clock(), self.current_sensor.read()])

    # Cell.time_delay does a time delay for the given amount of seconds while still logging
    def time_delay(self, seconds):
        start = time.clock()
        now = start
        while not self.die and (now - start) < seconds:
            now = time.clock()

    # Cell.charge_delay does a charge delay for the given amount of seconds while still logging
    def charge_delay(self, total_charge):
        charge = 0
        then = time.clock()
        then_current = self.current_sensor.read()

        while not self.die and charge < total_charge:
            now = time.clock()
            now_current = self.current
            charge += (now_current + then_current) * (now - then) / 2
            then = now
            then_current = now_current

    # Cell.set_bus_state sets the bus to the configured state
    def set_bus_state(self, sid):
        if not self.die:
            if sid == "S":
                self.bus.setstate([0, 0])
            elif sid == "A":
                self.bus.setstate([1, 0])
            elif sid == "B":
                self.bus.setstate([0, 1])
            elif sid == "C":
                self.bus.setstate([1, 1])
