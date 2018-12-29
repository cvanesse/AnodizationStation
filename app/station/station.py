# The station class is the highest level abstraction, it contains the cellhandlers for the station.
from .cellhandler import CellHandler
import os, json
from .logger import Logger
from .cyclebank import CycleBank

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))


class Station:

    cell_handlers = []
    LOGGER = Logger()
    CYCLEBANK = CycleBank()

    def __init__(self, cell_config):
        for cid in range(len(cell_config)):
            self.cell_handlers.append(CellHandler(cell_config[cid], cid))
        with open(os.path.join(SITE_ROOT, 'files/cellconfig.json')) as f:
            self.CELL_CONFIG = json.load(f)
