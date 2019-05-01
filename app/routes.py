from app import FLASK_APP, FLASK_LOGIN
from flask import render_template, request, json, url_for, redirect, send_from_directory
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
from app.station.station import Station
from app.forms import CycleUploadForm, LogDownloadForm, PowerForm
import os, time


SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
CYCLES_URL = os.path.join(SITE_ROOT, "files/cycles")
LOGS_URL = os.path.join(SITE_ROOT, "files/logs")
with open(os.path.join(SITE_ROOT, 'files/cellconfig.json')) as f:
    CELL_CONFIG = json.load(f)

STATION = Station(CELL_CONFIG)


@FLASK_APP.route('/power', methods=["GET", "POST"])
def power():
    form = PowerForm()
    title = "Power"
    if form.validate_on_submit():
        for cid in range(len(STATION.cell_handlers)):
            STATION.cell_handlers[cid].kill()

        cells_running = True
        while cells_running:
            cells_running = False
            for cid in range(len(STATION.cell_handlers)):
                cells_running = cells_running or STATION.cell_handlers[cid].cell_process.is_alive()

        if form.reboot.data:
            os.system('sudo reboot -h now')
            return redirect(url_for('power'))
        else:
            os.system('sudo shutdown -h now')
            return redirect(url_for('power'))
    return render_template("power.html", title=title, form=form)


@FLASK_APP.route('/')
@FLASK_APP.route('/index')
@FLASK_APP.route('/cellcontrol', methods=['GET'])
def render_cell_control():
    title = 'Cell Control'
    return render_template("cellcontrol.html", title=title, cycle_info=STATION.CYCLEBANK.CYCLE_INFO, cell_config=CELL_CONFIG)


@FLASK_APP.route('/cyclepage', methods=["GET", "POST"])
def render_cycle_page():
    title = 'Cycles'
    form = CycleUploadForm()
    if form.validate_on_submit():
        f = form.cyclefile.data
        filename = secure_filename(f.filename)
        f.save(os.path.join(CYCLES_URL, filename))
        STATION.CYCLEBANK.process_cycle_file(filename)
        redirect(url_for('render_cell_control'))
    return render_template("cycles.html", title=title, form=form)


@FLASK_APP.route('/logpage', methods=['GET', 'POST'])
def render_log_page():
    title = "Logs"
    form = LogDownloadForm()
    if form.validate_on_submit():
        STATION.LOGGER.update_log_info()
        date = form.date.data
        name = form.name.data
        try:
            filename = STATION.LOGGER.LOGS_INFO[date.strftime("%Y-%m-%d")][name]['file']
            if filename is not None:
                return send_from_directory(directory=LOGS_URL, filename=filename, as_attachment=True)
            else:
                redirect(url_for('render_cell_control'))
        except Exception as e:
            redirect(url_for('power'))

    return render_template("logs.html", title=title, form=form)


@FLASK_APP.route('/settings', methods=['GET'])
def render_settings_page():
    title = "Settings"
    return render_template("settings.html", title=title)


@FLASK_APP.route('/get_json', methods=['POST'])
def get_json():
    vals = request.values
    name = vals['name']

    if name == "CYCLE_INFO":
        ret = json.htmlsafe_dumps(STATION.CYCLEBANK.CYCLE_INFO)
    elif name == "LOGS_INFO":
        ret = json.htmlsafe_dumps(STATION.LOGGER.LOGS_INFO)
    elif name == "CELL_CONFIG":
        ret = json.htmlsafe_dumps(CELL_CONFIG)
    else:
        ret = ""

    return ret


@FLASK_APP.route('/run_cell', methods=['POST'])
def run_cell():
    info = request.get_json()
    cycle_id = info['cycle_id']
    cell_id = info['cell_id']
    cycle_params = info['cycle_params']
    num_cycles = info['num_cycles']
    sample_name = info['name']

    STATION.cell_handlers[cell_id].set_user('web')
    STATION.cell_handlers[cell_id].set_name(sample_name)
    STATION.cell_handlers[cell_id].set_num_cycles(num_cycles)
    STATION.cell_handlers[cell_id].set_cycle(STATION.CYCLEBANK.CYCLE_INFO[cycle_id]['file'])
    STATION.cell_handlers[cell_id].set_cycle_parameters(cycle_params)

    return STATION.cell_handlers[cell_id].run()


@FLASK_APP.route('/kill_cell', methods=['POST'])
def kill_cell():
    info = request.get_json()
    cell_id = info['cell_id']

    STATION.cell_handlers[cell_id].kill()

    while STATION.cell_handlers[cell_id].cell_process.is_alive():
        a = 1

    if STATION.cell_handlers[cell_id].try_join():
        ret = "Success"
    else:
        ret = "Fail"

    return ret


@FLASK_APP.route('/clear_cycles', methods=['POST'])
def clear_cycles():
    return STATION.CYCLEBANK.clear_cycles()


@FLASK_APP.route('/clear_logs', methods=['POST'])
def clear_logs():
    return STATION.LOGGER.clear_logs()


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
    return render_template("cellbox.html", cell_id=cid, cell_even=(cid % 2 == 0), cell_config=CELL_CONFIG[cid], cell_handler=STATION.cell_handlers[cid])


def render_cycle_params(cid, cyid):
    return render_template("cycleparams.html", all_cycle_info=STATION.CYCLEBANK.CYCLE_INFO, cycle_id=cyid, cell_id=cid)

