import time
import random
from PyQt5 import QtWidgets, QtCore, QtGui
        
class BonusWorker(QtCore.QThread):
    start_bonus = QtCore.pyqtSignal()
    stop_bonus = QtCore.pyqtSignal()

    def run(self):
        while True:
            self.start_bonus.emit()
            time.sleep(random.randint(6, 13)-3)
            time.sleep(3)
            self.stop_bonus.emit()
            time.sleep(random.randint(3, 5))
