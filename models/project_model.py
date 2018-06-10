from PyQt5.QtCore import QObject, QSemaphore, qDebug, pyqtSignal
from helpers.conformity_helper import ReplayThread
import json
from models.case_atribute_model import CaseAttributeModel
import sys
from multiprocessing import cpu_count

class ProjectModel(QObject):

    signal_project_has_changed = pyqtSignal()
    signal_conformity_algorithm_finished = pyqtSignal(str)

    def __init__(self,name="New Project"):
        super().__init__()
        self.name = name
        self.process_model = None
        self.case_attribute_model = []
        self.case_event_model = None

    def get_process_details(self):
        if self.process_model == None:
            data = {"process":None}
        else:
            name, n_nodes, n_transistions = self.process_model.details()
            data = {"process":str(name),"n_ativ":str(n_nodes),"n_trans":str(n_transistions)}
        retVal = json.dumps(data)
        return retVal

    def get_case_event_details(self):
        if self.case_event_model == None:
            data = {"case_log":None}
        else:
            name, n_cases, n_events = self.case_event_model.details()
            data = {"case_log": str(name), "n_cases": str(n_cases), "n_events": str(n_events)}
        retVal = json.dumps(data)
        return retVal

    def get_case_attribute_details(self):

        if len(self.case_attribute_model)==0:
            data = {"case_n":0}
        else:
            name, n_cases, n_attributes = self.case_attribute_model[0].details()
            data = {"case_n":str(len(self.case_attribute_model)),"case_log": str(name), "n_cases": str(n_cases), "n_attributes": str(n_attributes)}
        retVal = json.dumps(data)
        return retVal

    def get_project_name(self):
        return self.name


    def run_process_conformity(self,progress_bar,params=None):
        results = []
        nc = cpu_count() -1
        sem = QSemaphore(nc)
        qDebug("CPU count "+str(nc+1))
        parameters = json.loads(params)

        th_list = []
        n = len(self.case_event_model.cases)
        progress_bar.setMaximum(n)
        qDebug("Process Conformity -- Run")
        for (case, eventSeq) in self.case_event_model.cases.items():
            dummyCase = (case, eventSeq)
            th = ReplayThread(self.process_model,dummyCase,progress_bar,results,sem,params)
            th_list.append(th)
            th.start()
            sem.acquire()

        for th in th_list:
            if th.isFinished():
                th_list.remove(th)
            else:
                sem.acquire()

        n = 0
        nCase = CaseAttributeModel(name="Conformity Process Result")
        nCase.add_legend(["ID","Conformity"])
        string = ""
        for item in results:
            nCase.add_case(item[0],item[1:])
            string += str(item[0])+" : "+str(item[1])+" - "+str(item[2])+"\n"
            if not item[1]:
                n+=1
        if parameters["result_group"]=="append":
            self.case_attribute_model.append(nCase)
        elif parameters["result_group"]=="merge":
            self.case_attribute_model[0].merge(nCase,[0])

        self.signal_project_has_changed.emit()
        self.signal_conformity_algorithm_finished.emit(string)

        progress_bar.setValue(0)

    def export_case_attribute_log(self,file_path,progress_dialog=None,keep_legend_bool=True,delimiter=";"):
        self.case_attribute_model[0].export(file_path,progress_dialog,keep_legend_bool,delimiter)
