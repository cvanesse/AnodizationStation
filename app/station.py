# The station class is the highest level abstraction, it contains the cellhandlers for the station.
from .cellhandler import CellHandler
from .config import CELL_PARAMETERS


class Station:

    cell_handlers = []

    def __init__(self):
        for cid in range(len(CELL_PARAMETERS)):
            self.cell_handlers.append(CellHandler(CELL_PARAMETERS[cid]))
