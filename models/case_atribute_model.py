import csv
from models.case_model import CaseModel

class CaseAttributeModel(CaseModel):
    def details(self):
        name = self.name
        n_cases = len(self.cases)
        n_atributes = self.attribute_size
        return (name, n_cases, n_atributes)

    def create_from_file(self,origin_path,delimiter=";"):
        self.name = str(origin_path).split("/")[-1]
        file = open(origin_path)
        read = csv.reader(file, delimiter=delimiter)
        rows = []

        for row in read:
            rows.append(row)

        for row in rows[1:]:
            case = str(row[0])
            others = row[1:]
            self.attribute_size = len(others)
            self.cases[case] = [others]