from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtCore import QStringListModel


class CaseTableView(QTableWidget):

    def __init__(self,case_attribute_log):
        super().__init__()
        self.case = case_attribute_log
        self.setColumnCount(len(self.case.legend))
        self.setRowCount(len(self.case.cases))
        plegend = QStringListModel(self.case.legend).stringList()
        flegend = []
        for item in plegend:
            item = item.replace(" ","\n")
            flegend.append(item)
        self.setHorizontalHeaderLabels(flegend)
        self.setSortingEnabled(True)
        r=0
        for case, attr in self.case.cases.items():
            self.setItem(r,0,QTableWidgetItem(str(case)))
            c=1
            for att in attr[0]:
                self.setItem(r, c, QTableWidgetItem(str(att)))
                c+=1
            r+=1
