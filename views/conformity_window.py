from PyQt5.QtWidgets import QDialog, QDesktopWidget
from PyQt5 import uic
from PyQt5.QtCore import QObject, pyqtSignal, qDebug
import json

class ConformityWindow(QDialog):

    def __init__(self,parent,project):
        super().__init__(parent=parent)
        self.parent = parent
        self.project = project
        self.initUI()

    def initUI(self):
        self.ui = uic.loadUi('conformity_dialog.ui',self)
