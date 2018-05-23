from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon

from controllers.valinor_controler import Controller
from models.project_model import ProjectModel
from views.valinormainwindow import ValinorMainWindow


class ValinorApp(QApplication):

    def __init__(self,args):
        super().__init__(args)
        icon = QIcon()
        icon.addFile("resources/logo.jpg")
        self.setWindowIcon(icon)
        self.setApplicationName("Valinor App")

    def run(self):
        self.project = ProjectModel("Silmarillion")
        self.main_window = ValinorMainWindow(self.project)
        self.controller = Controller(self.main_window,self.project)
        self.main_window.show()