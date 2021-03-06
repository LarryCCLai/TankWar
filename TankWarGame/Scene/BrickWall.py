from PyQt5 import QtWidgets

class BrickWall(QtWidgets.QPushButton):
    def __init__(self, game_ui, x, y):
        super().__init__(game_ui)
        self.setText('')
        self.setStyleSheet('QPushButton{border-image:url(./TankWarGame/Image/scene/brick.png)}')
        self.setGeometry(x*game_ui.game_info.bsize, y*game_ui.game_info.bsize, game_ui.game_info.bsize, game_ui.game_info.bsize)                   
        self.setEnabled(False)