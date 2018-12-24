# The cell handler is the API for handling Cell initialization and running

from .cell import Cell
from multiprocessing import Process, Pipe
from .cycle import load_cycle


class CellHandler:

    # Cell Settings
    num_cycles = 0
    cycle_file = ''
    bus_pins = []
    log_file = ''

    # Multiprocessing variables
    cell_process = []
    handler_pipe = []

    # Cell State Variables
    cell_progress = []

    def __init__(self):
        # Default values for testing
        self.running_pin = 7
        self.bus_pins = [11, 15]
        self.cycle_file = 'tempfiles/test.cycle'
        self.num_cycle = 2
        self.log_file = 'tempfiles/test.csv'

    # This sets the cycle file which will be interpretted and passed to the cell when CellHandler.run() is called
    def set_cycle(self, newcycle):
        self.cycle_file = newcycle

    # This sets the log file which the cell will write to
    def set_log_file(self, newlog):
        self.log_file = newlog

    # This sets the pins which the cell will be initialized with when CellHandler.run() is called
    def set_bus_pins(self, newpins):
        self.bus_pins = newpins

    # This sets the number of cycles which is passed to the cell when CellHandler.run() is called
    def set_num_cycles(self, numcycles):
        self.num_cycles = numcycles

    # This sets the pin which outputs the "running" signal to the cell
    def set_running_pin(self, runningpin):
        self.running_pin = runningpin

    # This creates a Cell object
    def make_cell(self, cellpipe):
        cell = Cell(self.running_pin, self.bus_pins, self.log_file, cellpipe)
        cell_cycle = load_cycle(cell, self.cycle_file)
        cell.set_cycle(cell_cycle)
        return cell

    # This runs make_cell and cell.run_cycle(), needs to be run on a child process
    def run_cell(self, cellpipe):
        cell = self.make_cell(cellpipe)
        cell.run_cycle(self.num_cycles)

    # Starts a cell process with a pipe to communicate with it
    def run(self):
        [self.handler_pipe, cell_pipe] = Pipe(True)
        self.handler_pipe.send(False)
        self.cell_process = Process(target=self.run_cell, args=[cell_pipe])
        self.cell_process.start()

    # This checks for the progress of the cell.
    def check_cell(self):
        if self.handler_pipe.poll():
            while self.handler_pipe.poll():
                self.cell_progress = self.handler_pipe.recv()
            return self.cell_progress
        else:
            return self.cell_progress

    def kill(self):
        self.handler_pipe.send(True)

    # Tries to rejoin the cell process. Returns false if it cant
    def try_join(self):
        if not self.cell_process.is_alive():
            self.cell_process.join()
            return True
        else:
            return False
