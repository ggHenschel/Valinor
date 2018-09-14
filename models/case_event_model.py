from models.case_model import CaseModel
from PyQt5.QtCore import qDebug, QObject
import csv

class CaseEventModel(CaseModel):

    def __init__(self):
        super().__init__()
        self.n_cases = 0
        self.n_events = 0

    def create_from_file(self,origin_path,has_legend=False,delimiter=";"):
        self.name = str(origin_path).split("/")[-1]
        file = open(origin_path)
        read = csv.reader(file, delimiter=delimiter)
        rows = []

        self.n_cases = 0
        self.n_events = 0

        for row in read:
            rows.append(row)

        self.cases = dict()
        if has_legend:
            self.legend = rows[0]
            n=1
        else:
            n=0

        for row in rows[n:]:
            case = str(row[0])
            evento = row[1]
            timestampe = row[2]
            if case in self.cases:
                self.n_events+=1
                nx = self.cases[case]
                nx.append((evento, timestampe))
                nx.sort(key=lambda x: x[1])

            else:
                self.n_cases+=1
                self.n_events+=1
                self.cases[case] = [(evento, timestampe)]

    def details(self):
        name = self.name
        n_cases = self.n_cases
        n_events = self.n_events
        return (name,n_cases,n_events)
