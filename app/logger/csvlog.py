import csv


class CSVLog:

    wq = []

    def __init__(self, fp):
        self.filepath = fp

    def queue(self, row):
        self.wq.append(row)

    def writequeue(self):
        with open(self.filepath, 'a') as f:
            wr = csv.writer(f)
            wr.writerows(self.wq)
            self.wq = []

    def write(self, row):
        with open(self.filepath, 'a') as f:
            wr = csv.writer(f)
            wr.writerows(row)
