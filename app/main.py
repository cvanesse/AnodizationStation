# The main.py file calls:
#   - Initialization:
#       - Initialize station-specific cellhandlers
#       - Prepare callbacks for physical interface
#       - Start Flask Webserver
import os


def run():
    # Start the webserver
    os.environ["FLASK_APP"] = "app/flaskapp.py"
    os.system("flask run --host=0.0.0.0")
