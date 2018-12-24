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
def parse_cycle_file(filename, parameters):
    c = []
    a = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)

        parameter_names = []

        line1 = reader.__next__()
        if line1[0] == "Parameter Names:":
            # Here we need to define the local parameter variables which will hold inputs,
            # then check that we have the right amount of inputs
            for col in range(len(line1)):
                if not col == 0:
                    parameter_names.append(line1[col])

            if not len(parameter_names) == len(parameters):
                ValueError("Parameter number mismatch! len(parameters) must equal len(parameter_names)")
        else:
            c.append(line1[0])
            a.append(line1[1])

        for row in reader:
            c.append(row[0])
            if not len(parameter_names) == 0 and row[1] in parameter_names:
                pid = parameter_names.index(row[1])
                a.append(parameters[pid])
            else:
                a.append(row[1])

    cycle_commands = {
        'call_names': c,
        'call_args': a
    }

    return cycle_commands


# This turns the cycle_file into a list of commands and parameters bound to the Cell object
def load_cycle(cell, filename, parameters):
    cycle = Cycle()
    cycle_commands = parse_cycle_file(filename, parameters)
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
