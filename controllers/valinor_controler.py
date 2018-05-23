from PyQt5.QtCore import pyqtSlot, QObject
from helpers.import_helper import ImportHelper

class Controller(QObject):
    def __init__(self,main_window,project):
        super().__init__()
        self.main_window = main_window
        self.project = project
        self.create_connections()

    def create_connections(self):
        self.main_window.signal_import_process.connect(self.slot_import_process)
        self.main_window.signal_import_event_log.connect(self.slot_import_case_event_log)
        self.main_window.signal_import_atribute_log.connect(self.slot_import_case_attribute_log)


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
