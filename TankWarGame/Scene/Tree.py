from PyQt5 import QtWidgets, QtCore, QtGui

class Tree(QtWidgets.QPushButton):
    def __init__(self, game_ui):
        super().__init__(game_ui)
        self.setText('')
        self.setStyleSheet('QPushButton{border-image:url(./TankWarGame/Image/scene/tree.png)}')
                    