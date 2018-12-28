# This package contains all files needed to run the flask webserver which runs on the station
from flask import Flask
import os

FLASK_APP = Flask(__name__)
FLASK_APP.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'nchvisfnitsyci8435r34uiwt89'
FLASK_APP.add_url_rule("/files/cycles/<path:filename>", endpoint="cycles", view_func=FLASK_APP.send_static_file)

from app import routes
