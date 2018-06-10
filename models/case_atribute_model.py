from PyQt5.QtCore import qDebug
import csv
from models.case_model import CaseModel

class CaseAttributeModel(CaseModel):
    def details(self):
        name = self.name
        n_cases = len(self.cases)
        n_atributes = len(self.legend)
        return (name, n_cases, n_atributes)

    def create_from_file(self,origin_path,has_legend=False,delimiter=";"):
        self.name = str(origin_path).split("/")[-1]
        file = open(origin_path)
        read = csv.reader(file, delimiter=delimiter)
        rows = []

        for row in read:
            rows.append(row)

        if has_legend:
            self.legend=rows[0]
            n=1
        else:
            n=0

        for row in rows[n:]:
            case = str(row[0])
            others = row[1:]
            self.attribute_size = len(others)
            self.cases[case] = [others]

    def add_legend(self,legend):
        self.legend = legend

    def merge(self,newModel,list_of_itens):
        ilegend = newModel.legend
        for i in list_of_itens:
            self.legend.append(ilegend[i+1])

        for case, attr in self.cases.items():
            iitems = newModel.cases[case]
            for i in list_of_itens:
                attr[0].append(iitems[i])

    def export(self,file_path,progress_dialog=None,keep_legend_bool=True,delimiter=";"):
        with open(file_path,mode='w') as file:
            writer = csv.writer(file,delimiter=delimiter)
            if keep_legend_bool:
                writer.writerow(self.legend)

            progress_dialog.setMaximum(len(self.cases))
            n = 0
            progress_dialog.setValue(n)
            for case, attributes in self.cases.items():
                l = [case]
                for attribute in attributes[0]:
                    l.append(attribute)
                writer.writerow(l)
                n+=1


