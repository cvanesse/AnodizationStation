# The cell handler is the API for handling Cell initialization and running
from .cell import Cell
from multiprocessing import Process, Pipe
from .cyclebank import load_cycle


class CellHandler:

    # Cell Settings
    num_cycles = None
    cycle_file = None
    log_file = None
    cycle_parameters = None

    # Multiprocessing variables
    handler_pipe = []

    # Cell State Variables
    cell_progress = 0

    def __init__(self, cellconfig, cid):
        self.running_pin = cellconfig["running_pin"]
        self.bus_pins = cellconfig["bus_pins"]
        self.button_pin = cellconfig["button_pin"]
        self.cellID = cid
        self.cell_process = Process(target=self.run_cell)

    # This sets the cycle file which will be interpretted and passed to the cell when CellHandler.run() is called
    def set_cycle(self, newcycle):
        self.cycle_file = newcycle

    # This sets the log file which the cell will write to
    def set_log_file(self, newlog):
        self.log_file = newlog

    # This sets the number of cycles which is passed to the cell when CellHandler.run() is called
    def set_num_cycles(self, numcycles):
        self.num_cycles = numcycles

    # This sets the parameters which will be used while parsing the .cycle file
    def set_cycle_parameters(self, params):
        self.cycle_parameters = params.copy()

    # This creates a Cell object
    def make_cell(self, cellpipe):
        cell = Cell(self.running_pin, self.bus_pins, self.button_pin, cellpipe)
        cell_cycle = load_cycle(cell, self.cycle_file, self.cycle_parameters)
        cell.set_cycle(cell_cycle)
        return cell

    # This runs make_cell and cell.run_cycle(), needs to be run on a child process
    def run_cell(self, cellpipe):
        cell = self.make_cell(cellpipe)
        cell.run_cycle(self.num_cycles)

    # Starts a cell process with a pipe to communicate with it
    def run(self):
        if not (self.cycle_file is None or self.log_file is None or self.cycle_parameters is None or self.num_cycles is None):
            [self.handler_pipe, cell_pipe] = Pipe(True)
            self.try_join()
            self.cell_process = Process(target=self.run_cell, args=[cell_pipe])
            self.cell_process.start()
            return True
        else:
            RuntimeError("CellHandler not prepared! Please define all necessary parameters before running.")
            return False

    # This checks for the progress of the cell.
    def check_cell(self):
        if self.handler_pipe.poll():
            while self.handler_pipe.poll():
                self.cell_progress = self.handler_pipe.recv()
            return self.cell_progress
        else:
            return self.cell_progress

    # This tells the cell to die, so that it doesn't finish in the middle of an operation and corrupt anything.
    def kill(self):
        self.handler_pipe.send(True)

    # Tries to rejoin the cell process. Returns false if it cant
    def try_join(self):
        if (not self.cell_process.is_alive()) and (self.cell_process.pid is not None):
            self.cell_process.join()
            return True
        else:
            return False
