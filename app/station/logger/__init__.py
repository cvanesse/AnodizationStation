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

    # This function adds log information to logs.json
    #def add_log_to_database(self, filename, fileinfo):

    # This handles all the processing neceessary when a log is created
    #def process_log_file(self, filename, fileinfo):
    #    self.add_log_to_database(filename, fileinfo)


