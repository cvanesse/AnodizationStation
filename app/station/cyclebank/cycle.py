# The cycles file will handle everything to do with cycles
class Cycle:

    commands = []
    parameter_table = {}
    args = []
    call_names = []

    def __init__(self, cycle_info, cell):
        self.parameter_table = cycle_info['arg_dictionary']
        self.call_names = cycle_info['call_names']

        for cid in range(len(cycle_info['call_names'])):
            call_name = cycle_info['call_names'][cid]
            call_args = cycle_info['call_args'][cid]
            if call_name == 'time_delay':
                self.addcommand(cell.time_delay, call_args)
            elif call_name == 'charge_delay':
                self.addcommand(cell.charge_delay, call_args)
            elif call_name == 'set_state':
                self.addcommand(cell.set_bus_state, call_args)
            elif call_name == 'increment':
                #The first argument is the name of the parameter to increment
                #Swap this out with a parameter in the table
                self.parameter_table['i' + str(cid)] = call_args[0]
                call_args[0] = 'i' + str(cid)

                #Add a command which increments the desired parameter by the desired amount
                self.addcommand(self.increment_argument, call_args)

    def addcommand(self, command, arguments):
        self.commands.append(command)
        self.args.append(arguments)

    def run(self):
        for cid in range(len(self.commands)):
            c = self.commands[cid]
            if not isinstance(self.args[cid], (bytes, str)):
                a = [self.parameter_table[x] for x in self.args[cid]]
                c(*a)
            else:
                try:
                    a = self.parameter_table[self.args[cid]]
                    c(a)
                except:
                    raise Exception([self.call_names[cid], self.args[cid]])

    def increment_argument(self, name, incr):
        self.parameter_table[name] = self.parameter_table[name] + incr/10
