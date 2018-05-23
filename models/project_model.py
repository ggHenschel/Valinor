import json
class ProjectModel():
    def __init__(self,name="New Project"):
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

