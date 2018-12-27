from ..flaskapp import FLASK_APP
from flask import render_template, request, json
from ..station import Station
from ..cycle  import get_all_cycle_info

STATION = Station()

@FLASK_APP.route('/')
@FLASK_APP.route('/index')
@FLASK_APP.route('/cellcontrol', methods=['GET'])
def index():
    title = 'Cell Control'
    return render_template("cellcontrol.html", title=title, cellhandlers=STATION.cell_handlers, all_cycle_info=get_all_cycle_info(), cid=0)

@FLASK_APP.route('/cycles')
def cycles():
    title = 'Cycles'
    return render_template("cycles.html", title=title)

@FLASK_APP.route('/logs')
def logs():
    title = "Logs"
    return render_template("logs.html", title=title)


@FLASK_APP.route('/run_cell', methods=['POST'])
def run_cell():
    vals = request.values
    cell_id = int(vals['cell_id'])
    num_cycles = int(vals['num_cycles'])
    cycle_id = int(vals['cycle_id'])

    all_cycle_info = get_all_cycle_info()
    cycle_file = all_cycle_info[cycle_id]['filename']
    cycle_param_names = all_cycle_info[cycle_id]['parameters']

    cycle_params = []
    for pid in range(len(cycle_param_names)):
        cycle_params.append(vals[cycle_param_names[pid]])

    STATION.cell_handlers[cell_id].set_num_cycles(num_cycles)
    STATION.cell_handlers[cell_id].set_cycle(cycle_file)
    STATION.cell_handlers[cell_id].set_cycle_parameters(cycle_params)

    success = STATION.cell_handlers[cell_id].run()
    if success:
        return render_template("cellbox.html", cellhandler=STATION.cell_handlers[cell_id], all_cycle_info=get_all_cycle_info(), cid=0)
    else:
        return "Error!"


@FLASK_APP.route('/get_cycle_names', methods=['POST'])
def get_cycle_names():
    all_cycle_info = get_all_cycle_info()
    cycle_name_list = all_cycle_info[0]['displayname']
    for cid in range(len(all_cycle_info)):
        if cid is not 0:
            cycle_name_list = cycle_name_list + ',' + all_cycle_info[cid]['displayname']

    return cycle_name_list


@FLASK_APP.route('/get_cycle_param_names', methods=['POST'])
def get_cycle_params():
    vals = request.values
    cycle_id = int(vals['cycle_id'])
    params = get_all_cycle_info()[cycle_id]['parameters']
    param_list = params[0]
    for pid in range(len(params)):
        if pid is not 0:
            param_list = param_list + "," + params[pid]

    return param_list


@FLASK_APP.route('/get_cycle_param_display', methods=['POST'])
def get_cycle_param_display():
    vals = request.values
    cycle_id = int(vals['cycle_id'])
    cell_id = int(vals['cell_id'])
    return render_template('cycleparams.html', cellhandler=STATION.cell_handlers[cell_id], all_cycle_info=get_all_cycle_info(), cid=cycle_id)
