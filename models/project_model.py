from PyQt5.QtCore import QObject, QSemaphore, qDebug, pyqtSignal, pyqtSlot
from helpers.conformity_helper import ReplayThread
import json
from models.case_atribute_model import CaseAttributeModel
import sys
from multiprocessing import cpu_count

class ProjectModel(QObject):

    signal_project_has_changed = pyqtSignal()
    signal_conformity_algorithm_finished = pyqtSignal(str)
    signal_classification_algorithm_finished = pyqtSignal(str)
    signal_update_bar = pyqtSignal(int)

    def __init__(self,name="New Project"):
        super().__init__()
        self.name = name
        self.process_model = None
        self.case_attribute_model = []
        self.case_event_model = None
        self.attached_progess_bar = None

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
        bar_sem = QSemaphore(1)
        qDebug("CPU count "+str(nc+1))
        parameters = params
        self.attached_progess_bar = progress_bar

        th_list = []
        n = len(self.case_event_model.cases)
        progress_bar.setMaximum(n)
        qDebug("Process Conformity -- Run")
        for (case, eventSeq) in self.case_event_model.cases.items():
            dummyCase = (case, eventSeq)
            #qDebug("Start -- Case %s" % str(case))
            th = ReplayThread(self.process_model,dummyCase,progress_bar,bar_sem,results,sem,parameters)
            th.updateProgessbarSignal.connect(self.update_progress_bar_slot)
            th_list.append((th,case))
            th.start()
            sem.acquire()

        qDebug("All threads Created")

        for (th,case) in th_list:
            if th and th.isFinished():
                pass;
            else:
                sem.acquire()
            th.updateProgessbarSignal.disconnect(self.update_progress_bar_slot)


        n = 0
        nCase = CaseAttributeModel(name="Conformity Process Result")
        i_itens = []
        legend = ["ID"]
        if bool(parameters["conformity"]):
            legend.append(["Conformity"])
        if bool(parameters["types"]):
            legend.append(["NonConformity Type"])
        if parameters["notes"]=="add":
            legend.append(["Notes"])

        for i in range(len(legend)):
            i_itens.append(i)
        nCase.add_legend(legend)

        string = "Params:"
        for key, value in parameters.items():
            string += "\t" + str(key) + " : " + str(value) + "\n"

        string += "==============Report===========\n"
        for item in results:
            liste = []
            string += str(item[0]) + " : "
            if parameters["conformity"]:
                liste.append(item[1])
                string += str(item[1])+"\t"
            if parameters["types"]:
                liste.append(item[2])
                string += str(item[2])+"\t"
            if parameters["notes"]=="add":
                liste.append(str(item[3]))
            if parameters["notes"]!="ignore":
                string += str(item[3]) + "\t"
            nCase.add_case(item[0], liste)
            string+="\n"


        if parameters["result_group"] == "merge":
            self.case_attribute_model[0].merge(nCase,i_itens)

        self.attached_progess_bar.setValue(0)
        self.attached_progess_bar = None

        self.signal_project_has_changed.emit()
        self.signal_conformity_algorithm_finished.emit(string)

    def run_classification_algorithm(self,progress_bar,params=None):
        self.attached_progess_bar = progress_bar
        self.attached_progess_bar.setMaximum(100)
        self.attached_progess_bar.setValue(0)
        cc = self.case_attribute_model[0]
        (code, acc, dot_data, list) = cc.generate_tree(params)
        self.attached_progess_bar.setValue(50)
        #gera relatorio
        string = "Params:"
        for key, value in params.items():
            string+="\t"+str(key)+" : "+str(value)+"\n"

        string += "\n====================\nIgnored Attributes:\n"
        for item in list:
            string+="\t--"+self.case_attribute_model[0].legend[item+1]+"\n"
        string+="\n====================\nTree\n"+code+"\n====================\nAcurracy: "+str(acc)

        self.attached_progess_bar.setValue(100)
        self.signal_classification_algorithm_finished.emit(string)
        self.attached_progess_bar.setValue(0)
        self.attached_progess_bar = None

    def run_clustering_algorithm(self,progress_bar,params=None):
        self.attached_progess_bar = progress_bar
        self.attached_progess_bar.setMaximum(100)
        cc = self.case_attribute_model[0]
        self.signal_update_bar.emit(10)
        (centers, per_item) = cc.clustering_algorithm(params)
        self.signal_update_bar.emit(75)
        # gera relatorio
        string = "Params:"
        for key, value in params.items():
            string += "\t" + str(key) + " : " + str(value) + "\n"

        self.signal_update_bar.emit(80)

        string += "\n============\nIgnored Attributes:\n"
        for item in params["ignored_attributes"]:
            string += "\t--" + self.case_attribute_model[0].legend[item + 1] + "\n"
        string += "\n============\nClusters============\n"
        self.signal_update_bar.emit(85)
        cc=0
        for center in centers:
            string +=" "+str(cc)+" - "+str([format("%.5f"% x ) for x in center])+"\n"
            cc+=1
        string += "\n==========\nCluster per Case:==========\n"
        string += format("%14s -- Predicted Cluster\n" % "Case")
        self.signal_update_bar.emit(90)
        for item in per_item:
            string += format("%14s -- %4d\n" % (str(item[0]), int(item[1])))

        self.signal_update_bar.emit(100)
        self.signal_classification_algorithm_finished.emit(string)
        self.attached_progess_bar = None

    def export_case_attribute_log(self,file_path,progress_dialog=None,keep_legend_bool=True,delimiter=";"):
        self.case_attribute_model[0].export(file_path,progress_dialog,keep_legend_bool,delimiter)

    @pyqtSlot(int)
    def update_progress_bar_slot(self,value):
        v = self.attached_progess_bar.value()+value
        self.signal_update_bar.emit(v)
