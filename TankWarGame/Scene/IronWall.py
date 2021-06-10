from PyQt5 import QtWidgets, QtCore, QtGui

class IronWall(QtWidgets.QPushButton):
    def __init__(self, game_ui, x, y):
        super().__init__(game_ui)
        self.setText('')
        self.setStyleSheet('QPushButton{border-image:url(./TankWarGame/Image/scene/iron.png)}')
        self.setGeometry(x*game_ui.b_size, y*game_ui.b_size, game_ui.b_size, game_ui.b_size)                 
        self.setEnabled(False)