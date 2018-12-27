from ..flaskapp import FLASK_APP
from flask import render_template, request
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

@FLASK_APP.route('/cellcontrol', methods=['POST'])
def cell_control():
    cell_id = request.args['cell_id']
    num_cycles = request.args['num_cycles']
    STATION.cell_handlers[cell_id].set_num_cycles(num_cycles)
    success = STATION.cell_handlers[cell_id].run()
    return success
