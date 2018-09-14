from PyQt5.QtCore import QThread, qDebug, pyqtSignal

class ReplayThread(QThread):

    updateProgessbarSignal = pyqtSignal(int)

    def __init__(self,process, case, progress_bar,bar_sem, results, sem, params=None):
        super().__init__()
        self.process = process
        self.case = case
        self.params = params
        self.results = results
        self.progress_bar = progress_bar
        self.sem = sem
        self.bar_sem = bar_sem
        if params:
            self.export_type = bool(params["types"])
        else:
            self.export_type = True

    def run(self):
        case = str(self.case[0])
        #qDebug("Finished -- Case %s" % case)
        result = self.process.replay_case(self.case,self.export_type)
        self.results.append(result)
        #self.bar_sem.acquire()
        self.updateProgessbarSignal.emit(1)
        #self.bar_sem.release()
        self.sem.release()
