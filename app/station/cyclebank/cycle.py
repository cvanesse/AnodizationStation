# The cycles file will handle everything to do with cycles
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
