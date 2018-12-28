import csv


class CSVLog:

    wq = []

    def __init__(self, fp, tagNames):
        self.filepath = fp
        self.write(tagNames)

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
