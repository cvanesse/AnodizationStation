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
        if len(self.cyclecommands) == 0:
            self.cyclecommands = self.allcyclecommands
            self.cycleargs = self.allcycleargs

        command = self.cyclecommands.pop()
        args = self.cycleargs.pop()

        return command(args)
