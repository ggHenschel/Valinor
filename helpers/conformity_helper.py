from PyQt5.QtCore import QThread

class ReplayThread(QThread):

    def __init__(self,process, case, progess_bar, results,sem, params=None):
        super().__init__()
        self.process = process
        self.case = case
        self.params = params
        self.results = results
        self.progress_bar = progress_bar

    def run(self):
        result = self.process.replay_case(case)
        self.results.append(result)
