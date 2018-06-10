from PyQt5.QtWidgets import QFileDialog, QErrorMessage, QInputDialog, QMessageBox
from models.process_model import ProcessModel
from models.case_event_model import CaseEventModel
from models.case_atribute_model import CaseAttributeModel

class ImportHelper():

    def __init__(self):
        if self.this == None:
            self.this = self

    @staticmethod
    def import_process_model(project_model):
        n_process = ProcessModel()
        file, _ = QFileDialog.getOpenFileName(caption='Open File',filter="XML files (*.xml)")
        if file:
            try:
                n_process.create_from_file(file)
                project_model.process_model = n_process
                return True
            except Exception as e:
                dia = QErrorMessage()
                dia.setWindowTitle("Import Process Error")
                dia.showMessage("An Error Has Ocurred. Error:",str(e))
                return False
        else:
            return False

    @staticmethod
    def import_case_event_log(project_model):
        n_case = CaseEventModel()
        file, _ = QFileDialog.getOpenFileName(caption='Open File', filter="CSV files (*.csv)")
        if file:
            delimiterList = ["; (Semicolon)",", (Coma)","\\t (TAB)"," (SPACE)","Other"]
            delimiter, ok = QInputDialog.getItem(None,"Chose the Delimiter","Delimiter:",delimiterList)
            if not ok:
                return False
            option = delimiterList.index(delimiter)
            if option == 0:
                delimiter = ";"
            elif option == 1:
                delimiter = ","
            elif option == 2:
                delimiter = "\t"
            elif option == 3:
                delimiter = " "
            elif option == 4:
                delimiter, ok = QInputDialog.getText(None,"Type your Custom Delimiter","Delimiter")
                if not ok:
                    return False

            ret = QMessageBox().question(None, '', "Does your file contains a legend row?",
                                         QMessageBox.Yes | QMessageBox.No)

            if ret == QMessageBox.Yes:
                has_legend_bool = True
            else:
                has_legend_bool = False

            try:
                n_case.create_from_file(file,has_legend=has_legend_bool,delimiter=delimiter)
                project_model.case_event_model = n_case
                return True
            except Exception as e:
                print(e)
                return False
        else:
            return False

    @staticmethod
    def import_case_attribute_log(project_model):
        n_case = CaseAttributeModel()
        file, _ = QFileDialog.getOpenFileName(caption='Open File', filter="CSV files (*.csv)")
        if file:
            delimiterList = ["; (Semicolon)", ", (Coma)", "\\t (TAB)", " (SPACE)", "Other"]
            delimiter, ok = QInputDialog.getItem(None, "Chose the Delimiter", "Delimiter:", delimiterList)
            if not ok:
                return False
            option = delimiterList.index(delimiter)
            if option == 0:
                delimiter = ";"
            elif option == 1:
                delimiter = ","
            elif option == 2:
                delimiter = "\t"
            elif option == 3:
                delimiter = " "
            elif option == 4:
                delimiter, ok = QInputDialog.getText(None, "Type your Custom Delimiter", "Delimiter")
                if not ok:
                    return False


            ret = QMessageBox().question(None,'',"Does your file contains a legend row?", QMessageBox.Yes | QMessageBox.No)

            if ret == QMessageBox.Yes:
                has_legend_bool = True
            else:
                has_legend_bool = False
            try:
                n_case.create_from_file(file,has_legend=has_legend_bool,delimiter=delimiter)
                project_model.case_attribute_model.append(n_case)
                return True
            except Exception as e:
                print(e)
                return False
        else:
            return False
