# The cell handler is the API for handling Cell initialization and running

from .cell import Cell
from multiprocessing import Process
from .cycle import Cycle


class CellHandler:

    num_cycles = 0
    cycle_file = ''
    bus_pins = []
    log_file = ''
    cell_process = []

    def __init__(self):
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

    def parse_cycle_file(self):
        # TODO: Load and separate a csv file into function names and arguments
        cycle_commands = {
            'call_names': ['set_bus_state', 'time_delay', 'set_bus_state', 'time_delay'],
            'call_args': [[1], [0.5], [1], [0.5]]
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
                cycle.addcommand(Cell.time_delay, call_args)
            elif call_name == 'charge_delay':
                cycle.addcommand(Cell.charge_delay, call_args)
            elif call_name == 'set_bus_state':
                cycle.addcommand(Cell.set_bus_state, call_args)

        return cycle

    # This creates a Cell object
    def make_cell(self):
        cell = Cell(self.bus_pins, self.log_file)
        cell_cycle = self.load_cycle(cell)
        cell.set_cycle(cell_cycle)
        return cell

    def run_cell(self):
        cell = self.make_cell()
        cell.run_cycle(self.num_cycles)

    def run(self):
        self.cell_process = Process(self.run_cell)
        self.cell_process.run()

    def rejoin(self):
        self.cell_process.join()
