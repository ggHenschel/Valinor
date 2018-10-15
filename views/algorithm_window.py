from PyQt5.QtWidgets import QDialog
from PyQt5 import uic
from PyQt5.QtCore import QObject, pyqtSignal, qDebug, pyqtSlot,QTimer
from threading import Thread
from time import sleep
import json

class AlgorithmWindow(QDialog):

    signal_write_text = pyqtSignal(str)

    def __init__(self,parent,project):
        super().__init__(parent=parent)
        self.parent = parent
        self.project = project
        self.initUI()
        self.setup_connections()

    def initUI(self):
        self.ui = uic.loadUi('E:/Valinor/algorithm_dialog.ui',self)

    def setup_connections(self):
        self.ui.m_close_button.clicked.connect(self.cancel_button_clicked)
        self.ui.m_run_algorithm_button.clicked.connect(self.run_algorithm_button_clicked)

    def cancel_button_clicked(self):
        self.close()

    def run_algorithm_button_clicked(self):
        qDebug("Run Algorithm Button Clicked")
        self.progress_dialog = self.ui.m_progressBar
        self.th = Thread(target=self.algorithm_finished)
        self.th.start()
        self.signal_write_text.connect(self.write_text)

    def algorithm_finished(self):
        self.timer = QTimer()
        self.progress_dialog.setMaximum(100)
        n = 0
        while n!=100:
            self.progress_dialog.setValue(n)
            n+=1
            sleep(0.1)
        self.signal_write_text.emit("Algorithm Finished")
        self.progress_dialog.setMaximum(0)

    @pyqtSlot(str)
    def write_text(self,string):
        self.ui.m_textBrowser.setPlainText(string)
