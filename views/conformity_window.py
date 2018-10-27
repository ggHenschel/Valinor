from PyQt5.QtWidgets import QDialog
from PyQt5 import uic
from PyQt5.QtCore import QObject, pyqtSignal, qDebug, pyqtSlot
from threading import Thread
import json
from helpers.dev_utils import resource_path
from helpers.export_helper import ExportHelper

class ConformityWindow(QDialog):

    def __init__(self,parent,project):
        super().__init__(parent=parent)
        self.parent = parent
        self.project = project
        self.initUI()
        self.setup_connections()

    def initUI(self):
        self.ui = uic.loadUi(resource_path('conformity_dialog.ui'),self)

    def setup_connections(self):
        self.ui.m_close_button.clicked.connect(self.cancel_button_clicked)
        self.ui.m_run_algorithm_button.clicked.connect(self.run_algorithm_button_clicked)
        self.ui.m_exportResultButton.clicked.connect(self.slot_export_result_log)

    def cancel_button_clicked(self):
        self.close()

    def run_algorithm_button_clicked(self):
        qDebug("Run Algorithm Button Clicked")
        self.progress_dialog = self.ui.m_progressBar
        params = self.generate_params()
        self.th = Thread(target=self.project.run_process_conformity,args=[self.progress_dialog,params])
        self.th.start()
        self.ui.m_run_algorithm_button.setEnabled(False)
        self.project.signal_update_bar.connect(self.slot_update_bar)
        self.project.signal_conformity_algorithm_finished.connect(self.slot_project_has_finished)
        self.ui.m_exportResultButton.setEnabled(False)

    def generate_params(self):
        data = dict()
        result_group = str("show_only")
        if self.ui.m_rg_merge.isChecked():
            result_group = str("merge")

        data["result_group"] = result_group

        if self.ui.m_rb_ann_add.isChecked():
            data["notes"] = str("add")
        elif self.ui.m_rb_ann_show.isChecked():
            data["notes"] = str("show")
        elif self.ui.m_rb_ann_ignore.isChecked():
            data["notes"] = str("ignore")

        data["types"] = self.ui.m_conformity_type.isChecked()
        data["conformity"] = self.ui.m_conformity_export.isChecked()
        params = data
        return params


    @pyqtSlot(str)
    def slot_project_has_finished(self,jdata):
        self.ui.m_textBrowser.setPlainText(jdata)
        self.project.signal_update_bar.disconnect(self.slot_update_bar)
        self.project.signal_conformity_algorithm_finished.disconnect(self.slot_project_has_finished)
        self.ui.m_run_algorithm_button.setEnabled(True)
        self.ui.m_exportResultButton.setEnabled(True)

    @pyqtSlot(int)
    def slot_update_bar(self,v):
        self.progress_dialog.setValue(v)

    @pyqtSlot()
    def slot_export_result_log(self):
        ExportHelper.export_result_log(self.ui.m_textBrowser.toPlainText(),"conformity")
