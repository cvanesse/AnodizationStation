# This package contains all files needed to run the flask webserver which runs on the station
from flask import Flask
import os
from ..flaskapp import routes

FLASK_APP = Flask(__name__)
FLASK_APP.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'nchvisfnitsyci8435r34uiwt89'

def start_webserver():
    os.environ["FLASK_APP"] = "../main.py"
