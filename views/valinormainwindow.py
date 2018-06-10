from PyQt5.QtWidgets import QMainWindow, QDesktopWidget
from PyQt5 import uic
from PyQt5.QtCore import QObject, pyqtSignal, qDebug, QTimer, pyqtSlot
from views.conformity_window import ConformityWindow
from views.algorithm_window import AlgorithmWindow
from views.case_attribute_table_view import CaseTableView
import json, sys

class ValinorMainWindow(QMainWindow):

    signal_import_process = pyqtSignal()
    signal_import_event_log = pyqtSignal()
    signal_import_attribute_log = pyqtSignal()
    signal_export_attribute_log = pyqtSignal()

    def __init__(self,project=None):
        super().__init__()

        self.project = project
        self.init_UI()
        self.conformity_window = None
        self.has_case_attribute_tab = False


    def init_UI(self):
        self.ui = uic.loadUi('valinormainwindow.ui',self)
        self.setWindowTitle('Valinor App - '+str(self.project.get_project_name()))
        self.timer = QTimer()
        self.init_status_bar()
        self.project_updated()
        self.set_connections()
        self.ui.m_about_textBrowser.setHtml(open("resources/about.html").read())


    def init_status_bar(self):
        self.ui.statusBar().showMessage('Finished Loading')
        self.timer.singleShot(500,self.clear_status_bar_message)

    def project_updated(self):
        process_data = json.loads(self.project.get_process_details())
        if process_data["process"] == None:
            process_string = "[No Process Model Loaded]"
            process_loaded = False
        else:
            process_loaded = True
            process_string = "["+process_data["process"]+" | "+process_data["n_ativ"]+" activities | "+process_data["n_trans"]+" transicions]"

        case_event_data = json.loads(self.project.get_case_event_details())
        if case_event_data["case_log"] == None:
            case_event_string = "[No Case Event Data Loaded]"
            case_event_loaded = False
        else:
            case_event_loaded = True
            case_event_string = "["+case_event_data["case_log"]+" | "+case_event_data["n_cases"]+" cases | "+case_event_data["n_events"]+" events]"

        case_attribute_data = json.loads(self.project.get_case_attribute_details())
        if case_attribute_data["case_n"]== 0:
            case_attribute_string = "[No Case Attribute Data Loaded]"
            self.ui.m_classifierButton.setEnabled(False)
            self.ui.m_clusteringButton.setEnabled(False)
        else:
            case_attribute_string = "["+case_attribute_data["case_log"]+" | "+case_attribute_data["n_cases"]+" cases | "+case_attribute_data["n_attributes"]+" attributes]"
            if int(case_attribute_data["case_n"])>1:
                case_attribute_string += " [+"+str(int(case_attribute_data["case_n"])-1)+"]"
            self.handle_case_table_view()
            self.ui.m_classifierButton.setEnabled(True)
            self.ui.m_clusteringButton.setEnabled(True)

        self.ui.m_processLabel.setText(process_string)
        self.ui.m_caseEventLogLabel.setText(case_event_string)
        self.ui.m_caseAtributteLabel.setText(case_attribute_string)
        if process_loaded and case_event_loaded:
            self.ui.m_conformityButton.setEnabled(True)
        else:
            self.ui.m_conformityButton.setEnabled(False)

    def set_connections(self):
        self.ui.m_importProcessModelButton.clicked.connect(self.import_process_model_button_clicked)
        self.ui.actionImport_Process.triggered.connect(self.import_process_model_button_clicked)
        self.ui.m_importCaseEventLogButton.clicked.connect(self.import_case_event_log_button_clicked)
        self.ui.m_importCaseAttributeButton.clicked.connect(self.import_case_attribute_log_button_clicked)
        self.ui.m_conformityButton.clicked.connect(self.conformity_window_button_clicked)
        self.ui.m_exportCaseAtributeLogButton.clicked.connect(self.export_case_attribute_log_button_clicked)
        self.ui.m_classifierButton.clicked.connect(self.classifier_window_button_cliked)
        self.ui.m_clusteringButton.clicked.connect(self.clustering_window_button_cliked)

    def import_process_model_button_clicked(self):
        self.signal_import_process.emit()

    def import_case_event_log_button_clicked(self):
        self.signal_import_event_log.emit()

    def import_case_attribute_log_button_clicked(self):
        self.signal_import_attribute_log.emit()

    def conformity_window_button_clicked(self):
        self.conformity_window = ConformityWindow(self,self.project)
        self.conformity_window.show()

    def classifier_window_button_cliked(self):
        self.classifier_algorithm_window = AlgorithmWindow(self, self.project)
        self.classifier_algorithm_window.show()

    def clustering_window_button_cliked(self):
        self.clustering_algorithm_window = AlgorithmWindow(self, self.project)
        self.clustering_algorithm_window.show()

    def export_case_attribute_log_button_clicked(self):
        self.signal_export_attribute_log.emit()

    def set_status_bar_message(self,message,t=-1):
        self.ui.statusBar().showMessage(message)
        if t!=-1:
            self.timer.singleShot(t*1000, self.clear_status_bar_message)

    def handle_case_table_view(self):
        self.table_view = CaseTableView(self.project.case_attribute_model[0])
        if self.has_case_attribute_tab:
            self.ui.m_tabWidget.removeTab(self.case_attribute_tab)
            self.has_case_attribute_tab = True

        self.case_attribute_tab = self.ui.m_tabWidget.addTab(self.table_view,"Case Attribute")
        self.table_view.show()

    @pyqtSlot()
    def clear_status_bar_message(self):
        self.ui.statusBar().clearMessage()