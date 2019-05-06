import csv, os, datetime, base64

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
LOGS_URL = os.path.join(SITE_ROOT, "../../files/logs")


class CSVLog:

    wq = []

    def __init__(self, filename=None, tagnames=None):
        if filename is not None:
            self.filename = filename + "_"
            self.filename = self.filename + self.generate_log_filename()
            self.filename = self.filename + ".csv"
        else:
            self.filename = self.generate_log_filename()

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
            f.flush()
            f.close()

    def write(self, row):
        with open(self.filepath, 'a') as f:
            wr = csv.writer(f)
            wr.writerow(row)
            f.flush()
            f.close()

    # This function creates a log filename which hasnt been used yet.
    def generate_log_filename(self):
        now = datetime.datetime.now()
        return str(base64.urlsafe_b64encode(str(now).encode('ascii'))) + '.csv'
