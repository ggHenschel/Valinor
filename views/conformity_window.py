from PyQt5.QtWidgets import QDialog
from PyQt5 import uic
from PyQt5.QtCore import QObject, pyqtSignal, qDebug, pyqtSlot
from threading import Thread
import json

class ConformityWindow(QDialog):

    def __init__(self,parent,project):
        super().__init__(parent=parent)
        self.parent = parent
        self.project = project
        self.initUI()
        self.setup_connections()

    def initUI(self):
        self.ui = uic.loadUi('conformity_dialog.ui',self)

    def setup_connections(self):
        self.ui.m_close_button.clicked.connect(self.cancel_button_clicked)
        self.ui.m_run_algorithm_button.clicked.connect(self.run_algorithm_button_clicked)

    def cancel_button_clicked(self):
        self.close()

    def run_algorithm_button_clicked(self):
        qDebug("Run Algorithm Button Clicked")
        self.progress_dialog = self.ui.m_progressBar
        params = self.generate_params()
        self.th = Thread(target=self.project.run_process_conformity,args=[self.progress_dialog,params])
        self.th.start()
        self.project.signal_conformity_algorithm_finished.connect(self.slot_project_has_finished)

    def generate_params(self):
        data = dict()
        result_group = str("show_only")
        if self.ui.m_rg_merge.isChecked():
            result_group = str("merge")
        elif self.ui.m_rg_append.isChecked():
            result_group = str("append")

        data["result_group"] = result_group

        if self.ui.m_ag_nonconforme_checkbox.isChecked():
            activity_conformity_option = str("non_conform")
        else:
            activity_conformity_option = str("not_selected")

        data["activity_conformity_option"] = activity_conformity_option
        data["types"] = str(self.ui.m_conformity_type.isChecked())
        params = json.dumps(data)
        return params


    @pyqtSlot(str)
    def slot_project_has_finished(self,jdata):
        self.ui.m_textBrowser.setPlainText(jdata)
        self.project.signal_conformity_algorithm_finished.disconnect(self.slot_project_has_finished)
