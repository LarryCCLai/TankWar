from PyQt5 import QtWidgets

class Border(QtWidgets.QPushButton):
    def __init__(self, game_ui, x, y):
        super().__init__(game_ui)
        self.setText('')
        self.setStyleSheet("QPushButton{background-color:#808080}")
        self.setGeometry(x*game_ui.game_info.bsize, y*game_ui.game_info.bsize, game_ui.game_info.bsize, game_ui.game_info.bsize)            
        self.setEnabled(False)