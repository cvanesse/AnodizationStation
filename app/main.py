# The main.py file calls:
#   - Initialization:
#       - Initialize station-specific cellhandlers
#       - Prepare callbacks for physical interface
#       - Start Flask Webserver
from .cellhandler import CellHandler
from .webhandler import start_webserver
from .config import CELL_PARAMETERS


def run():
    # Initialize CellHandlers
    cellhandlers = []
    for cid in range(len(CELL_PARAMETERS)):
        cellhandlers.append(CellHandler(CELL_PARAMETERS[cid]))

    # Start the webserver
    start_webserver()

    return cellhandlers
