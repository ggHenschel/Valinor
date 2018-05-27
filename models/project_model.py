from PyQt5.QtCore import QObject, QSemaphore
from helpers.conformity_helper import ReplayThread
import json
import sys
from multiprocessing import cpu_count

class ProjectModel(QObject):
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
        n = cpu_count() -1
        sem = QSemaphore(n)
        th_list = []
        for (case, eventSeq) in self.case_event_model.cases.items():
            dummyCase = (case, eventSeq)
            th = ReplayHelper(self.process_model,dummyCase,progress_bar,results,sem,params)
            th_list.append(th)
            th.start()
            sem.acquire()

        for th in th_list:
            th.join()

        print(results)
