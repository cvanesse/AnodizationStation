# Try to import the GPIO library, otherwise initialize differently
try:
    from RPi import GPIO

    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)

    RASPBERRY = True
except:
    RASPBERRY = False


# We import different pins and busses based on the system we're working with
if RASPBERRY:
    from .gpioPin import GPIOPin as ExtPin
    from .gpioBus import GPIOBus as ExtBus
else:
    from .terminalPin import TerminalTestPin as ExtPin
    from .terminalBus import TerminalBus as ExtBus


class Pin(ExtPin):
    pass


class Bus(ExtBus):
    pass




