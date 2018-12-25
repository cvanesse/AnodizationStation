# This package contains all files needed to run the flask webserver which runs on the station
from flask import Flask
import os

FLASK_APP = Flask(__name__)

from ..flaskapp import routes


def start_webserver():
    os.environ["FLASK_APP"] = "../main.py"