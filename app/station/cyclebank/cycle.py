# The cycles file will handle everything to do with cycles
class Cycle:

    commands = []
    parameter_table = {}
    args = []

    def __init__(self, cycle_info, cell):
        self.parameter_table = cycle_info['arg_dictionary']

        for cid in range(len(cycle_info['call_names'])):
            call_name = cycle_info['call_names'][cid]
            call_args = cycle_info['call_args'][cid]
            if call_name == 'time_delay':
                self.addcommand(cell.time_delay, call_args)
            elif call_name == 'charge_delay':
                self.addcommand(cell.charge_delay, call_args)
            elif call_name == 'set_bus_state':
                self.addcommand(cell.set_bus_state, call_args)
            elif call_name == 'increment':
                self.parameter_table['i' + str(cid)] = call_args[0]
                call_args[0] = 'i' + str(cid)
                self.addcommand(self.increment_argument, call_args)

    def addcommand(self, command, arguments):
        self.commands.append(command)
        self.args.append(arguments)

    def run(self):
        for cid in range(len(self.commands)):
            c = self.commands[cid]
            a = [self.parameter_table[x] for x in self.args[cid]]
            c(*a)

    def increment_argument(self, name, incr):
        self.parameter_table[name] = self.parameter_table[name] + incr
