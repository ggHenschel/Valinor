from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtCore import QStringListModel


class CaseTableView(QTableWidget):

    def __init__(self,case_attribute_log):
        super().__init__()
        self.case = case_attribute_log
        self.setColumnCount(len(self.case.legend))
        self.setRowCount(len(self.case.cases))
        legend = QStringListModel(self.case.legend).stringList()
        self.setHorizontalHeaderLabels(legend)
        self.setSortingEnabled(False)
        r=0
        for case, attr in self.case.cases.items():
            self.setItem(r,0,QTableWidgetItem(str(case)))
            c=1
            for att in attr[0]:
                self.setItem(r, c, QTableWidgetItem(str(att)))
                c+=1
            r+=1
