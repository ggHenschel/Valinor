from views.algorithm_window import AlgorithmWindow
from PyQt5.QtWidgets import QDialog
from PyQt5 import uic
from PyQt5.QtCore import QObject, pyqtSignal, qDebug, pyqtSlot,QTimer
from threading import Thread
from time import sleep
import json

class ClassificationWindow(AlgorithmWindow):


    def initUI(self):
        self.ui = uic.loadUi('E:/Valinor/classification_algorithm_dialog.ui',self)
        self.ui.m_cl_class.clear()
        self.ui.m_cl_class.addItems(self.project.case_attribute_model[0].legend[1:])
        self.ui.m_cl_class.setCurrentIndex(len(self.project.case_attribute_model[0].legend[1:])-1)

    def run_algorithm_button_clicked(self):
        self.progress_dialog = self.ui.m_progressBar
        params = self.generate_params()
        self.th = Thread(target=self.project.run_classification_algorithm,args=[self.progress_dialog,params])
        self.th.start()
        self.ui.m_run_algorithm_button.setEnabled(False)
        self.project.signal_update_bar.connect(self.slot_update_bar)
        self.project.signal_classification_algorithm_finished.connect(self.slot_project_has_finished)

    def generate_params(self):
        data = params = {"max_features": None,
                  "min_sample_split": 2,
                  "min_sample_leafs": 1,
                  "min_weight_fraction_leaf": 0.0,
                  "random_state": None,
                  "max_leaf_nodes": None,
                  "min_impurity_split": None,
                  "ignored_attributes": [],
                  "code_type": "j48"
                  }
        data["class_index"]=self.ui.m_cl_class.currentIndex()
        if self.ui.m_rg_entropy.isChecked():
            data["criterion"]="entropy"
        else:
            data["criterion"] = "gini"

        data["perct_of_test"] = float(self.ui.m_sb_percent.value())/100

        if self.ui.m_rg_splitter_best.isChecked():
            data["splitter"]="best"
        else:
            data["splitter"] = "random"

        data["max_depth"] = int(self.ui.m_sb_max_depth.value())

        params = data
        return params

    @pyqtSlot(str)
    def slot_project_has_finished(self, jdata):
        self.ui.m_textBrowser.setPlainText(jdata)
        self.project.signal_update_bar.disconnect(self.slot_update_bar)
        self.project.signal_classification_algorithm_finished.disconnect(self.slot_project_has_finished)
        self.ui.m_run_algorithm_button.setEnabled(True)

    @pyqtSlot(int)
    def slot_update_bar(self,v):
        self.progress_dialog.setValue(v)
