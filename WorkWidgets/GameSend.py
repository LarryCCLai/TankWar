from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import pyqtSignal
import json

class GameSend(QtCore.QThread):
    def __init__(self, clinet, command, params):
        super().__init__()
        self.params = params
        self.client = clinet
        self.command = command
    def run(self):
        self.client.send_command(self.command, self.params)
        