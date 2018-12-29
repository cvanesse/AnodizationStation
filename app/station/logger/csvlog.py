import csv, os
from ..logger import generate_log_filename

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
LOGS_URL = os.path.join(SITE_ROOT, "../../files/logs")


class CSVLog:

    wq = []

    def __init__(self, filename=None, tagnames=None):
        if filename is not None:
            self.filename = filename
        else:
            self.filename = generate_log_filename()

        self.filepath = os.path.join(LOGS_URL, self.filename)

        if tagnames is not None:
            self.write(tagnames)

    def queue(self, row):
        self.wq.append(row)

    def write_queue(self):
        with open(self.filepath, 'a') as f:
            wr = csv.writer(f)
            wr.writerows(self.wq)
            self.wq = []

    def write(self, row):
        with open(self.filepath, 'a') as f:
            wr = csv.writer(f)
            wr.writerow(row)
