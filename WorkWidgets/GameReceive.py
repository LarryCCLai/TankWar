from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal
import json

class GameReceive(QtCore.QThread):
    return_sig = pyqtSignal(str)
    def __init__(self, clinet):
        super().__init__()
        self.client = clinet
        self.flag = True

    def terminate(self):
        self.flag = False
        
    def run(self):
        while(self.flag):
            response = self.client.wait_response()
            self.return_sig.emit(json.dumps(response))
        
