from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal
import json


class ExecuteCommand(QtCore.QThread):
    return_sig = pyqtSignal(str)

    def __init__(self, clinet, command, params):
        super().__init__()
        self.params = params
        self.client = clinet
        self.command = command
    def run(self):
        self.client.send_command(self.command, self.params)
        response = self.client.wait_response()
        self.return_sig.emit(json.dumps(response))
        