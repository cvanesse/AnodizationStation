# The cell handler is the API for handling Cell initialization and running

from .cell import Cell
from multiprocessing import Process, Pipe
from .cycle import Cycle
import csv


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
        #Default values for testing
        self.running_pin = 7
        self.bus_pins = [11, 15]
        self.cycle_file = 'tempfiles/test.cycle'
        self.num_cycle = 2
        self.log_file = 'tempfiles/test.csv'
        self.cell_progress = 0
        pass

    # This sets self.cycle_file
    def set_cycle(self, newcycle):
        self.cycle_file = newcycle

    # This sets self.log_file
    def set_log_file(self, newlog):
        self.log_file = newlog

    # This sets self.bus_pins
    def set_bus_pins(self, newpins):
        self.bus_pins = newpins

    def set_num_cycles(self, numcycles):
        self.num_cycles = numcycles

    def set_running_pin(self, runningpin):
        self.running_pin = runningpin

    def parse_cycle_file(self):
        C = []
        A = []
        with open(self.cycle_file, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                C.append(row[0])
                A.append(row[1])

        cycle_commands = {
            'call_names': C,
            'call_args': A
        }

        return cycle_commands

    # This turns the cycle_file into a list of commands and parameters bound to the Cell object
    def load_cycle(self, Cell):
        cycle = Cycle()
        cycle_commands = self.parse_cycle_file()
        for cid in range(len(cycle_commands['call_names'])):
            call_name = cycle_commands['call_names'][cid]
            call_args = cycle_commands['call_args'][cid]
            if call_name == 'time_delay':
                cycle.addcommand(Cell.time_delay, float(call_args))
            elif call_name == 'charge_delay':
                cycle.addcommand(Cell.charge_delay, float(call_args))
            elif call_name == 'set_bus_state':
                cycle.addcommand(Cell.set_bus_state, call_args)

        return cycle

    # This creates a Cell object
    def make_cell(self, cellpipe):
        cell = Cell(self.running_pin, self.bus_pins, self.log_file, cellpipe)
        cell_cycle = self.load_cycle(cell)
        cell.set_cycle(cell_cycle)
        return cell

    # This runs make_cell and cell.run_cycle(), needs to be run on a child process
    def run_cell(self, cellpipe):
        cell = self.make_cell(cellpipe)
        cell.run_cycle(self.num_cycles)

    # Starts a cell process with a pipe to communicate with it
    def run(self):
        [self.handler_pipe, cell_pipe] = Pipe(True)
        self.cell_process = Process(target=self.run_cell, args=cell_pipe)
        self.cell_process.start()

    def check_cell(self):
        if self.handler_pipe.poll():
            self.cell_progress = self.handler_pipe.recv()
            return self.cell_progress
        else:
            return self.cell_progress

    def kill(self):
        self.handler_pipe.send(True)

    # Rejoins the cell process
    def rejoin(self):
        self.cell_process.join()
