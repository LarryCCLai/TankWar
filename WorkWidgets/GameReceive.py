from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import pyqtSignal
import json

class GameReceive(QtCore.QThread):
    return_sig = pyqtSignal(str)
    def __init__(self, clinet):
        super().__init__()
        self.client = clinet
    def run(self):
        while(True):
            response = self.client.wait_response()
            self.return_sig.emit(json.dumps(response))
        
