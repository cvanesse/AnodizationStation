# The cycles file will handle everything to do with cycles
import csv


# It will not hold the "runcycle" function, that it a member of the cell class
class Cycle:

    commands = []
    args = []

    def __init__(self):
        pass

    def addcommand(self, command, arguments):
        self.commands.append(command)
        self.args.append(arguments)

    def run(self):
        for cid in range(len(self.commands)):
            c = self.commands[cid]
            a = self.args[cid]
            c(a)


# This parses a cycle file
def parse_cycle_file(filename):
    c = []
    a = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            c.append(row[0])
            a.append(row[1])

    cycle_commands = {
        'call_names': c,
        'call_args': a
    }

    return cycle_commands


# This turns the cycle_file into a list of commands and parameters bound to the Cell object
def load_cycle(cell, filename):
    cycle = Cycle()
    cycle_commands = parse_cycle_file(filename)
    for cid in range(len(cycle_commands['call_names'])):
        call_name = cycle_commands['call_names'][cid]
        call_args = cycle_commands['call_args'][cid]
        if call_name == 'time_delay':
            cycle.addcommand(cell.time_delay, float(call_args))
        elif call_name == 'charge_delay':
            cycle.addcommand(cell.charge_delay, float(call_args))
        elif call_name == 'set_bus_state':
            cycle.addcommand(cell.set_bus_state, call_args)

    return cycle
