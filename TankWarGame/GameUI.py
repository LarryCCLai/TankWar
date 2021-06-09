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

class GameUI(QtWidgets.QFrame):
    def __init__(self, widget):
        super().__init__(widget)
        self.setGeometry( 0,  0, game_ui_width, game_ui_height)
        self.setStyleSheet('QWidget{background-color:black;}') 
        self.map_dict = Map().read_map()
        self.generate_scene()

    def generate_scene(self):
        for dim in self.map_dict:
            scene = sence_dict[self.map_dict[dim]](self)
            scene.setGeometry(dim[0]*b_size, dim[1]*b_size, b_size, b_size)
