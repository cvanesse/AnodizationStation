# This package contains all files needed to run the flask webserver which runs on the station
from flask import Flask
from flask_login import LoginManager
from werkzeug.contrib.fixers import ProxyFix
import os

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))

FLASK_APP = Flask(__name__)
FLASK_APP.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'nchvisfnitsyci8435r34uiwt89'
FLASK_APP.config['UPLOAD_FOLDER'] = os.path.join(SITE_ROOT, 'files/uploads')
FLASK_LOGIN = LoginManager(FLASK_APP)
FLASK_LOGIN.login_view = 'render_login_page'

from app import routes

FLASK_APP.wsgi_app = ProxyFix(FLASK_APP.wsgi_app)

if __name__ == '__main__':
    FLASK_APP.run()
