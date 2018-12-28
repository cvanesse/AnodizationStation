from app import FLASK_APP
from flask import render_template, request, json, url_for
from app.station.station import Station
import os


SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
CYCLES_URL = os.path.join(SITE_ROOT, "files/cycles")
LOGS_URL = os.path.join(SITE_ROOT, "files/logs")
with open(os.path.join(CYCLES_URL, 'cycles.json')) as f:
    CYCLE_INFO = json.load(f)
with open(os.path.join(LOGS_URL, 'logs.json')) as f:
    LOGS_INFO = json.load(f)
with open(os.path.join(SITE_ROOT, 'files/cellconfig.json')) as f:
    CELL_CONFIG = json.load(f)

STATION = Station(CELL_CONFIG)


@FLASK_APP.route('/')
@FLASK_APP.route('/index')
@FLASK_APP.route('/cellcontrol', methods=['GET'])
def render_cell_control():
    title = 'Cell Control'
    return render_template("cellcontrol.html", title=title, cell_config=CELL_CONFIG, json_cycle_info=CYCLE_INFO, json_cell_config=CELL_CONFIG)


@FLASK_APP.route('/cyclepage')
def render_cycle_page():
    title = 'Cycles'
    return render_template("cycles.html", title=title)


@FLASK_APP.route('/logpage')
def render_log_page():
    title = "Logs"
    return render_template("logs.html", title=title)


@FLASK_APP.route('/get_json', methods=['POST'])
def get_json():
    vals = request.values
    name = vals['name']

    if name == "CYCLE_INFO":
        ret = json.htmlsafe_dumps(CYCLE_INFO)
    elif name == "LOGS_INFO":
        ret = json.htmlsafe_dumps(LOGS_INFO)
    elif name == "CELL_CONFIG":
        ret = json.htmlsafe_dumps(CELL_CONFIG)
    else:
        ret = ""

    return ret


@FLASK_APP.route('/run_cell', methods=['POST'])
def run_cell():
    info = request.get_json()
    print(info)
    cycle_id = info['cycle_id']
    cell_id = info['cell_id']
    cycle_params = info['cycle_params']
    num_cycles = info['num_cycles']

    STATION.cell_handlers[cell_id].set_num_cycles(num_cycles)
    STATION.cell_handlers[cell_id].set_cycle(CYCLE_INFO[cycle_id]['file'])
    STATION.cell_handlers[cell_id].set_cycle_parameters(cycle_params)

    success = STATION.cell_handlers[cell_id].run()

    if success:
        return "Cell started."
    else:
        return "Error while starting cell."

@FLASK_APP.route('/render', methods=['POST'])
def do_render():
    info = request.get_json()
    name = info['name']

    if name == "cellbox":
        cell_id = int(info['cell_id'])
        return render_cellbox(cid=cell_id)
    elif name == "cycleparams":
        cell_id = int(info['cell_id'])
        cycle_id = int(info['cycle_id'])
        return render_cycle_params(cid=cell_id, cyid=cycle_id)

    return "<p>Error!</p>"


def render_cellbox(cid):
    return render_template("cellbox.html", cell_id=cid, cell_config=CELL_CONFIG[cid], cell_handler=STATION.cell_handlers[cid])


def render_cycle_params(cid, cyid):
    return render_template("cycleparams.html", all_cycle_info=CYCLE_INFO, cycle_id=cyid, cell_id=cid)
