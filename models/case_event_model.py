from models.case_model import CaseModel
import csv

class CaseEventModel(CaseModel):

    def __init__(self):
        super().__init__()
        self.n_cases = 0
        self.n_events = 0

    def create_from_file(self,origin_path,delimiter=";"):
        self.name = str(origin_path).split("/")[-1]
        file = open(origin_path)
        read = csv.reader(file, delimiter=delimiter)
        rows = []

        self.n_cases = 0
        self.n_events = 0

        for row in read:
            rows.append(row)

        self.cases = dict()

        for row in rows[1:]:
            case = str(row[0])
            evento = row[1]
            timestampe = row[2]
            if case in self.cases:
                self.n_events+=1
                nx = self.cases[case]
                nx.append((evento, timestampe))
            else:
                self.n_cases+=1
                self.n_events+=1
                self.cases[case] = [(evento, timestampe)]

    def details(self):
        name = self.name
        n_cases = self.n_cases
        n_events = self.n_events
        return (name,n_cases,n_events)