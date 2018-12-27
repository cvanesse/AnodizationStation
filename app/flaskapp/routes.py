from ..flaskapp import FLASK_APP
from flask import render_template, request, json
from ..station import Station

STATION = Station()

@FLASK_APP.route('/')
@FLASK_APP.route('/index')
@FLASK_APP.route('/cellcontrol', methods=['GET'])
def index():
    title = 'Cell Control'
    return render_template("cellcontrol.html", title=title, cellhandlers=STATION.cell_handlers)

@FLASK_APP.route('/cycles')
def cycles():
    title = 'Cycles'
    return render_template("cycles.html", title=title)

@FLASK_APP.route('/logs')
def logs():
    title = "Logs"
    return render_template("logs.html", title=title)


@FLASK_APP.route('/run_cell', methods=['POST'])
def cell_control():
    vals = request.values
    cell_id = int(vals['cell_id'])
    num_cycles = int(vals['num_cycles'])
    STATION.cell_handlers[cell_id].set_num_cycles(num_cycles)
    success = STATION.cell_handlers[cell_id].run()
    if success:
        return render_template("cellbox.html", cellhandler=STATION.cell_handlers[cell_id])
    else:
        return "Error!"

@FLASK_APP.route('/get_cellbox', methods=['GET'])
def get_cellbox():
    vals = request.values
    cell_id = int(vals['cell_id'])
    return render_template("cellbox.html", cellhandler=STATION.cell_handlers[cell_id])
