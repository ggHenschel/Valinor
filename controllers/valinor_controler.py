from PyQt5.QtCore import pyqtSlot, QObject
from PyQt5.QtWidgets import QProgressDialog
from helpers.import_helper import ImportHelper
from helpers.export_helper import ExportHelper

class Controller(QObject):
    def __init__(self,main_window,project):
        super().__init__()
        self.main_window = main_window
        self.project = project
        self.create_connections()

    def create_connections(self):
        self.main_window.signal_import_process.connect(self.slot_import_process)
        self.main_window.signal_import_event_log.connect(self.slot_import_case_event_log)
        self.main_window.signal_import_attribute_log.connect(self.slot_import_case_attribute_log)
        self.project.signal_project_has_changed.connect(self.slot_project_has_changed)
        self.main_window.signal_export_attribute_log.connect(self.slot_export_case_attribute_log)


    @pyqtSlot()
    def slot_import_process(self):
        if ImportHelper.import_process_model(self.project):
            self.main_window.project_updated()

    @pyqtSlot()
    def slot_import_case_event_log(self):
        if ImportHelper.import_case_event_log(self.project):
            self.main_window.project_updated()

    @pyqtSlot()
    def slot_import_case_attribute_log(self):
        if ImportHelper.import_case_attribute_log(self.project):
            self.main_window.project_updated()

    @pyqtSlot()
    def slot_project_has_changed(self):
        self.main_window.project_updated()

    @pyqtSlot()
    def slot_export_case_attribute_log(self):
        self.main_window.set_status_bar_message("Exporting Log",-1)
        progress_dialog = QProgressDialog()
        if ExportHelper.export_case_attribute_log(self.project,progress_dialog):
            self.main_window.set_status_bar_message("Log Exported",3)
        else:
            self.main_window.set_status_bar_message("Export Failed", 3)
