# The main.py file calls:
#   - Initialization:
#       - Initialize station-specific cellhandlers
#       - Prepare callbacks for physical interface
#       - Start Flask Webserver
from .cellhandler import CellHandler
from .config import CELL_PARAMETERS
import os


def run():
    # Initialize CellHandlers
    cellhandlers = []
    for cid in range(len(CELL_PARAMETERS)):
        cellhandlers.append(CellHandler(CELL_PARAMETERS[cid]))

    # Start the webserver
    os.environ["FLASK_APP"] = "app/flaskapp.py"
    os.system("flask run")

    return cellhandlers
