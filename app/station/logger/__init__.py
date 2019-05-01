from .csvlog import CSVLog
import datetime, base64, os, json, shutil


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

    # Deletes all .csv log files and clears the JSON database
    def clear_logs(self):
        try:
            # Clears the Logs Folder
            shutil.rmtree(LOGS_URL)
            os.mkdir(LOGS_URL)

            # Create an empty cycles.json file
            with open(os.path.join(LOGS_URL, 'logs.json'), 'a') as f:
                f.writelines(json.dumps({}))

            with open(os.path.join(LOGS_URL, 'logs.json')) as f:
                self.LOGS_INFO = json.load(f)

            return "Success"
        except:
            return "Fail"


# This function adds log information to logs.json
def add_log_to_database(file_info, name, date):
    database_filename = os.path.join(LOGS_URL, 'logs.json')

    with open(database_filename) as f:
        LOGS_INFO = json.load(f)

    if not date in LOGS_INFO:
        LOGS_INFO[date] = {}
    LOGS_INFO[date][name] = file_info

    os.remove(database_filename)

    with open(database_filename, 'w') as f:
        f.writelines(json.dumps(LOGS_INFO, sort_keys=True, indent=2))
