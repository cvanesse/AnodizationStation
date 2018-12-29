# The station class is the highest level abstraction, it contains the cellhandlers for the station.
from .cellhandler import CellHandler
import os, json
from .cycle import get_cycle_info

cell_handlers = []
SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
SITE_ROOT = os.path.join(SITE_ROOT, '../')
CYCLES_URL = os.path.join(SITE_ROOT, "files/cycles")
LOGS_URL = os.path.join(SITE_ROOT, "files/logs")


class Station:

    cell_handlers = []

    def __init__(self, cell_config):
        for cid in range(len(cell_config)):
            self.cell_handlers.append(CellHandler(cell_config[cid], cid))

        with open(os.path.join(CYCLES_URL, 'cycles.json')) as f:
            self.CYCLE_INFO = json.load(f)
        with open(os.path.join(LOGS_URL, 'logs.json')) as f:
            self.LOGS_INFO = json.load(f)
        with open(os.path.join(SITE_ROOT, 'files/cellconfig.json')) as f:
            self.CELL_CONFIG = json.load(f)

    def process_cycle_file(self, filename):
        cycle_info = get_cycle_info(os.path.join(CYCLES_URL, filename))

        cycle_entry = {
            'name': cycle_info[0],
            'file': filename,
            'parameters': cycle_info[1]
        }

        self.CYCLE_INFO.append(cycle_entry)

        database_filename = os.path.join(CYCLES_URL, 'cycles.json')
        os.remove(database_filename)

        with open(os.path.join(CYCLES_URL, 'cycles.json'), 'w') as f:
            f.writelines(json.dumps(self.CYCLE_INFO))
