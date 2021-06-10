from PyQt5 import QtWidgets, QtGui, QtCore
from TankWarGame.Scene.Border import Border
from  TankWarGame.Scene.IronWall import IronWall
from  TankWarGame.Scene.BrickWall import BrickWall
from  TankWarGame.Scene.Tree import Tree
from  TankWarGame.Scene.Home import Home
from  TankWarGame.Map.Map import Map

b_size = 24
game_ui_width = 840
game_ui_height = 672

sence_dict = {
    1:Tree,
    2:BrickWall,
    3:IronWall,
    4:Home,
}

class StatUI(QtWidgets.QFrame):
    def __init__(self, Form):
        super().__init__(Form)
        self.setGeometry(QtCore.QRect(840, 0, 240, 672))
        self.setStyleSheet("background-color:#808080") 
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        self.setObjectName("stat")

    