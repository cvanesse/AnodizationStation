import os


def run():
    # Start the webserver
    os.environ["FLASK_APP"] = "runflask.py"
    os.system("flask run --host=0.0.0.0")


run()
