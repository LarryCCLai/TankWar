from PyQt5 import QtWidgets, QtCore, QtGui

class BrickWall(QtWidgets.QPushButton):
    def __init__(self, game_ui):
        super().__init__(game_ui)
        self.setText('')
        self.setStyleSheet('QPushButton{border-image:url(./TankWarGame/Image/scene/brick.png)}')
                    