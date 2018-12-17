# The cycles file will handle everything to do with cycles


# It will not hold the "runcycle" function, that it a member of the cell class
class Cycle:

    allcyclecommands = []
    allcycleargs = []
    cyclecommands = []
    cycleargs = []

    def __init__(self):
        pass

    def addcommand(self, command, arguments):
        self.allcyclecommands.append(command)
        self.allcycleargs.append(arguments)

    def pop(self):
        if len(self.cyclecommands) < 1:
            self.refill()

        command = self.cyclecommands.pop(0)
        args = self.cycleargs.pop(0)

        return command(args)

    def refill(self):
        self.cyclecommands = self.allcyclecommands.copy()
        self.cycleargs = self.allcycleargs.copy()
