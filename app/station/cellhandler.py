# The cell handler is the API for handling Cell initialization and running
from .cell import Cell
from multiprocessing import Process, Pipe
from .cyclebank import load_cycle


class CellHandler:

    # Cell Settings
    num_cycles = None
    cycle_file = None
    cycle_parameters = None
    name = None
    user = None

    # Multiprocessing variables
    handler_pipe = []

    # Cell State Variables
    cell_progress = 0

    def __init__(self, cellconfig, cid):
        self.cell_config = cellconfig
        self.cellID = cid
        self.cell_process = Process(target=self.run_cell)

    # This sets the cycle file which will be interpretted and passed to the cell when CellHandler.run() is called
    def set_cycle(self, newcycle):
        self.cycle_file = newcycle

    # This sets the number of cycles which is passed to the cell when CellHandler.run() is called
    def set_num_cycles(self, numcycles):
        self.num_cycles = numcycles

    # This sets the parameters which will be used while parsing the .cycle file
    def set_cycle_parameters(self, params):
        self.cycle_parameters = params.copy()

    def set_user(self, user):
        self.user = user

    def set_name(self, name):
        self.name = name

    # This runs make_cell and cell.run_cycle(), needs to be run on a child process
    def run_cell(self, cellpipe):
        cell = Cell(self.cell_config, self.user, self.name, cellpipe)
        cell_cycle = load_cycle(cell, self.cycle_file, self.cycle_parameters)
        cell.set_cycle(cell_cycle)
        cell.run_cycle(self.num_cycles)

    # Starts a cell process with a pipe to communicate with it
    def run(self):
        try:
            [self.handler_pipe, cell_pipe] = Pipe(True)
            self.try_join()
            self.cell_process = Process(target=self.run_cell, args=[cell_pipe])
            self.cell_process.start()
            return "Success"
        except Exception as e:
            return e

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
        if self.cell_process.is_alive():
            self.handler_pipe.send(True)

    # Tries to rejoin the cell process. Returns false if it cant
    def try_join(self):
        if (not self.cell_process.is_alive()) and (self.cell_process.pid is not None):
            self.cell_process.join()
            return True
        else:
            return False
