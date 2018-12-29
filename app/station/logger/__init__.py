from .csvlog import CSVLog
import datetime, base64, os, json


SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
SITE_ROOT = os.path.join(SITE_ROOT, '../../')
LOGS_URL = os.path.join(SITE_ROOT, "files/logs")


class Logger:

    LOGS_INFO = []

    # At initialization, we need to locate the log info file and
    def __init__(self):
        with open(os.path.join(LOGS_URL, 'logs.json')) as f:
            self.LOGS_INFO = json.load(f)

    # This handles all the processing neceessary when a log is created
    def update_log_info(self):
        with open(os.path.join(LOGS_URL, 'logs.json')) as f:
            self.LOGS_INFO = json.load(f)


# This function adds log information to logs.json
def add_log_to_database(file_info):
    database_filename = os.path.join(LOGS_URL, 'logs.json')

    with open(database_filename) as f:
        LOGS_INFO = json.load(f)

    LOGS_INFO.append(file_info)

    os.remove(database_filename)

    with open(database_filename, 'w') as f:
        f.writelines(json.dumps(LOGS_INFO, sort_keys=True, indent=2))
