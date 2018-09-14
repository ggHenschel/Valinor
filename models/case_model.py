import csv
from PyQt5.QtCore import QObject

class CaseModel(QObject):

    def __init__(self,name='A Case has no name'):
        super().__init__()
        self.cases = dict()
        self.name = name
        self.attribute_size = None

    # def create_from_file(self,origin_path,delimiter=";"):
    #     self.name = str(origin_path).split("/")[-1]
    #     file = open(origin_path)
    #     read = csv.reader(file, delimiter=delimiter)
    #     rows = []
    #
    #     for row in read:
    #         rows.append(row)
    #
    #     for row in rows[1:]:
    #         case = str(row[0])
    #         others = row[1:]
    #         self.attribute_size = len(others)
    #         print(others)
    #         self.cases[case] = [others]

    def get_name(self):
        return self.name

    def add_case(self,case,atributes):
        self.cases[case]=atributes
