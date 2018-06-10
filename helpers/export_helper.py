from PyQt5.QtWidgets import QFileDialog, QErrorMessage, QInputDialog, QMessageBox, QProgressDialog
from models.process_model import ProcessModel
from models.case_event_model import CaseEventModel
from models.case_atribute_model import CaseAttributeModel

class ExportHelper():

    def __init__(self):
        if self.this == None:
            self.this = self

    @staticmethod
    def export_case_attribute_log(project,progress_dialog):
        file_path, ok = QFileDialog.getSaveFileName(None,None,"Save Log",options=QFileDialog.DontUseCustomDirectoryIcons,filter="CSV files (*.csv)")
        if not ok:
            return False
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
        ret = QMessageBox().question(None, '', "Does your file contains a legend row?",
                                     QMessageBox.Yes | QMessageBox.No)

        if ret == QMessageBox.Yes:
            keep_legend_bool = True
        else:
            keep_legend_bool = False

        if len(project.case_attribute_model)>1:
            ret = QMessageBox().question(None, '', "Your Project has more than 1 attribute Model.\nDo you want to export the first one?\n",                                         QMessageBox.Yes | QMessageBox.Cancel)
            if ret == QMessageBox.Cancel:
                return False

        progress_dialog.show()
        project.export_case_attribute_log(file_path,progress_dialog,keep_legend_bool,delimiter)
        progress_dialog.close()

        return True