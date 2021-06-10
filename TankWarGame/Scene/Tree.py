from PyQt5 import QtWidgets, QtCore, QtGui

class Tree(QtWidgets.QPushButton):
    def __init__(self, game_ui, x, y):
        super().__init__(game_ui)
        self.setText('')
        self.setStyleSheet('QPushButton{border-image:url(./TankWarGame/Image/scene/tree.png)}')
        self.setGeometry(x*game_ui.game_info.bsize, y*game_ui.game_info.bsize, game_ui.game_info.bsize, game_ui.game_info.bsize)
                    