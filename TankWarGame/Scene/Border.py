from PyQt5 import QtWidgets, QtCore, QtGui

class Border(QtWidgets.QPushButton):
    def __init__(self, game_ui):
        super().__init__(game_ui)
        self.setText('')
        self.setStyleSheet("QPushButton{background-color:#808080}")
                    