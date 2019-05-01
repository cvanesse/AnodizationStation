from .gpiocontrol import Bus, Pin
from .logger import CSVLog, add_log_to_database
from .pisense import CurrentSensor, DigiPinSensor
import time, datetime
from threading import Thread


# The Cell should be created within the same subprocess that runs Cell.run_cycle
class Cell:

    # These will eventually be set during initialization of the program
    ina_address = 0x40
    tag_names = ['Time [s]', 'Cycle Number', 'Cell State', 'Current [mA]']

    # We read sensors and log data on a separate thread from the control thread
    sensor_thread = []
    keep_sensing = False
    current = []

    # We need a way to communicate with the CellHandler, and a state variable for various signals
    cell_pipe = []
    die = []

    #Some state variables, for logging purposes
    state = 'S'
    cycle_num = 0

    def __init__(self, cell_config, user, name, cellpipe):
        self.user = user
        self.name = name
        self.bus = Bus(cell_config['bus_pins'])
        self.running_pin = Pin(cell_config['running_pin'])
        #self.button = DigiPinSensor(cell_config['button_pin'])
        self.ina_address = cell_config['ina_address']
        #self.button.add_callback(self.kill)
        self.log = CSVLog(tagnames=self.tag_names)
        self.current_sensor = CurrentSensor(self.ina_address)
        self.cell_pipe = cellpipe
        self.cell_pipe.send(0)
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

        # Add the log file to the database
        add_log_to_database({
            'file': self.log.filename,
            'user': self.user,
            'time': str(datetime.datetime.now())
        }, self.name, datetime.datetime.now().strftime("%Y-%m-%d"))

        #Run the cycle the specified number of times
        for i in range(numcycles):
            if self.die:
                break
            self.cycle_num = i + 1
            self.cycle.run()
            self.cell_pipe.send(i + 1)

        #Tell the sensing thread to stop, then rejoin the sensor thread
        self.keep_sensing = False
        sensor_thread.join()

        #Short the cell output, and set the running pin to 0, to ensure safe shutdown.
        self.set_bus_state('S')
        self.running_pin.setstate(0)

    # The loop run on the designated sensing thread
    # The sensing thread handles reading sensors and checking for a kill signal from the CellHandler
    def sensor_loop(self):
        start = time.perf_counter()
        while self.keep_sensing:
            now = time.perf_counter()
            self.current = self.current_sensor.read()
            self.log.write([now-start, self.cycle_num, self.state, self.current])
            if self.cell_pipe.poll():
                self.die = self.cell_pipe.recv()

    # Cell.time_delay does a time delay for the given amount of seconds while still logging
    def time_delay(self, seconds):
        start = time.perf_counter()
        now = start
        while not self.die and (now - start) < float(seconds):
            now = time.perf_counter()

    # Cell.charge_delay does a charge delay for the given amount of seconds while still logging
    def charge_delay(self, total_charge):
        total_charge = float(total_charge)
        charge = 0
        then = time.perf_counter()
        then_current = self.current_sensor.read()

        while not self.die and charge < total_charge:
            now = time.perf_counter()
            now_current = self.current_sensor.read()  # This is a hack, find a way to communicate with logger thread
            charge = charge + (now_current + then_current) * (now - then) / 2
            then = now
            then_current = now_current

    # Cell.set_bus_state sets the bus to the configured state
    def set_bus_state(self, sid):
        self.state = sid
        if not self.die:
            if sid == "S":
                self.bus.setstate([0, 0])
            elif sid == "A":
                self.bus.setstate([1, 0])
            elif sid == "B":
                self.bus.setstate([0, 1])
            elif sid == "C":
                self.bus.setstate([1, 1])

    def kill(self, channel):
        self.die = True
