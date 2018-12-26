from ..flaskapp import FLASK_APP
from flask import render_template

@FLASK_APP.route('/')
@FLASK_APP.route('/index')
@FLASK_APP.route('/cellcontrol')
def index():
    title = 'Cell Control'
    return render_template("cellcontrol.html", title=title)

@FLASK_APP.route('/cycles')
def cycles():
    title = 'Cycles'
    return render_template("cycles.html", title=title)

@FLASK_APP.route('/logs')
def logs():
    title = "Logs"
    return render_template("logs.html", title=title)
