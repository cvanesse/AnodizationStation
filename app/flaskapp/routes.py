from ..flaskapp import FLASK_APP

@FLASK_APP.route('/')
@FLASK_APP.route('/index')
def index():
    return "Hello World!"
