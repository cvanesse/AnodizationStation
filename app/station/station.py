# The station class is the highest level abstraction, it contains the cellhandlers for the station.
from .cellhandler import CellHandler


class Station:

    cell_handlers = []

    def __init__(self, cell_config):
        for cid in range(len(cell_config)):
            self.cell_handlers.append(CellHandler(cell_config[cid], cid))
