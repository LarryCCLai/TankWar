from PyQt5 import QtWidgets, QtGui, QtCore
from  TankWarGame.Scene.Tree import Tree

class Background(QtWidgets.QFrame):
    def __init__(self, Form, game_info):
        super().__init__(Form)
        self.game_info = game_info
        self.setGeometry( 0,  0, game_info.game_ui_width, game_info.game_ui_height)
        self.setStyleSheet('QWidget{background-color:black;}') 
        for dim in game_info.map_dict:
            if(game_info.map_dict[dim] != game_info.tree):
                continue
            game_info.static_objs[dim] = Tree(self, dim[0], dim[1])