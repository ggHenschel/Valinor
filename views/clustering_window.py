from views.algorithm_window import AlgorithmWindow
from PyQt5.QtWidgets import QDialog
from PyQt5 import uic
from PyQt5.QtCore import QObject, pyqtSignal, qDebug, pyqtSlot, QTimer
from threading import Thread
from time import sleep
import json

class ClusteringWindow(AlgorithmWindow):


    def initUI(self):
        self.ui = uic.loadUi('clustering_dialog.ui',self)

    def run_algorithm_button_clicked(self):
        self.progress_dialog = self.ui.m_progressBar
        params = self.generate_params()
        self.th = Thread(target=self.project.run_clustering_algorithm,args=[self.progress_dialog,params])
        self.th.start()
        self.ui.m_run_algorithm_button.setEnabled(False)
        self.project.signal_classification_algorithm_finished.connect(self.slot_project_has_finished)

    def generate_params(self):
        data = {
              "mode":"k-means++", #"random"
              "number_of_clusters":2,
              "n_init":10,
              "max_iter":300,
              "tolerance":float(1e-4),
              "random_state":True,
              "algorithm":"auto", #full, elkan,
              "ignored_attributes": []}

        if self.ui.m_rg_kmeans.isChecked():
            data["mode"] = "k-means++"
        else:
            data["mode"] = "random"

        if self.ui.m_rb_alg_auto.isChecked():
            data["algorithm"] = "auto"
        elif self.ui.m_rb_alg_full.isChecked():
            data["algorithm"] = "full"
        else:
            data["algorithm"] = "elkan"

        data["number_of_clusters"] = int(self.ui.m_sb_n_clusters.value())
        data["max_iter"] = int(self.ui.m_sb_max_iter.value())

        params = data
        return params

    @pyqtSlot(str)
    def slot_project_has_finished(self, jdata):
        self.ui.m_textBrowser.setPlainText(jdata)
        self.project.signal_classification_algorithm_finished.disconnect(self.slot_project_has_finished)
        self.ui.m_run_algorithm_button.setEnabled(True)

