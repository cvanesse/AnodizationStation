#This is a sensor emulator which can be used for testing on a PC
#It just responds with a random value between 0 and 10
import random
from .sensor import Sensor


class RandomSensor(Sensor):

    def __init__(self):
        Sensor.__init__(self)

    def read(self):
        return random.uniform(0, 10)
