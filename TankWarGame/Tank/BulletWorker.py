import time
import random
from PyQt5 import QtWidgets, QtCore, QtGui

class BulletWorker(QtCore.QThread):
    done_singnal = QtCore.pyqtSignal()
    def __init__(self, bullet):
        super().__init__()
        self.bullet = bullet
    
    def run(self):
        while self.bullet.life:
            self.bullet.move()
            time.sleep(0.02)
        self.done_singnal.emit()