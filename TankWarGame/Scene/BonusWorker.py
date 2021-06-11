import time
import random
from PyQt5 import QtWidgets, QtCore, QtGui
        
class BonusWorker(QtCore.QThread):
    start_bonus = QtCore.pyqtSignal()
    stop_bonus = QtCore.pyqtSignal()

    def run(self):
        while True:
            self.start_bonus.emit()
            time.sleep(15)
            self.stop_bonus.emit()
            time.sleep(random.randint(5, 10))
