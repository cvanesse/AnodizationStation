from app import FLASK_APP, FLASK_LOGIN
from flask import render_template, request, json, url_for, redirect, send_from_directory
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
from flask_login import current_user, login_user, login_required, logout_user
from app.station.station import Station
from app.forms import LoginForm, CycleUploadForm, LogDownloadForm
from app.models import User
import os


SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
CYCLES_URL = os.path.join(SITE_ROOT, "files/cycles")
LOGS_URL = os.path.join(SITE_ROOT, "files/logs")
with open(os.path.join(SITE_ROOT, 'files/cellconfig.json')) as f:
    CELL_CONFIG = json.load(f)

STATION = Station(CELL_CONFIG)


@FLASK_APP.route('/login', methods=["GET", "POST"])
def render_login_page():
    form = LoginForm()
    title = "Sign In"
    if form.validate_on_submit():
        proposed_user = User(form.username.data)
        if proposed_user.phash is None or not check_password_hash(proposed_user.phash, form.password.data):
            return redirect(url_for('render_login_page'))
        login_user(proposed_user, remember=form.remember_me.data)
        return redirect(url_for('render_cell_control'))
    return render_template("login.html", title=title, form=form)


@FLASK_APP.route('/logout', methods=["GET"])
def logout():
    logout_user()
    return redirect(url_for('render_login_page'))


@FLASK_APP.route('/')
@FLASK_APP.route('/index')
@FLASK_APP.route('/cellcontrol', methods=['GET'])
@login_required
def render_cell_control():
    title = 'Cell Control'
    return render_template("cellcontrol.html", title=title, cycle_info=STATION.CYCLEBANK.CYCLE_INFO, cell_config=CELL_CONFIG)


@FLASK_APP.route('/cyclepage', methods=["GET", "POST"])
@login_required
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
@login_required
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
                redirect(url_for('render_log_page'))
        except Exception as e:
            redirect(url_for('render_log_page'))

    return render_template("logs.html", title=title, form=form)


@FLASK_APP.route('/get_json', methods=['POST'])
@login_required
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
@login_required
def run_cell():
    info = request.get_json()
    cycle_id = info['cycle_id']
    cell_id = info['cell_id']
    cycle_params = info['cycle_params']
    num_cycles = info['num_cycles']
    sample_name = info['name']

    STATION.cell_handlers[cell_id].set_user(current_user.uname)
    STATION.cell_handlers[cell_id].set_name(sample_name)
    STATION.cell_handlers[cell_id].set_num_cycles(num_cycles)
    STATION.cell_handlers[cell_id].set_cycle(STATION.CYCLEBANK.CYCLE_INFO[cycle_id]['file'])
    STATION.cell_handlers[cell_id].set_cycle_parameters(cycle_params)

    return STATION.cell_handlers[cell_id].run()


@FLASK_APP.route('/render', methods=['POST'])
@login_required
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
    return render_template("cycleparams.html", all_cycle_info=STATION.CYCLEBANK.CYCLE_INFO, cycle_id=cyid, cell_id=cid)
