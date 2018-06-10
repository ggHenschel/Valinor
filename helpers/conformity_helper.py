from PyQt5.QtCore import QThread, qDebug

class ReplayThread(QThread):

    def __init__(self,process, case, progress_bar, results, sem, params=None):
        super().__init__()
        self.process = process
        self.case = case
        self.params = params
        self.results = results
        self.progress_bar = progress_bar
        self.sem = sem

    def run(self):
        result = self.process.replay_case(self.case)
        self.results.append(result)
        value = int(self.progress_bar.value())+1
        self.progress_bar.setValue(int(value))
        self.sem.release()
