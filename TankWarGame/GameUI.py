from PyQt5 import QtWidgets, QtGui, QtCore
from TankWarGame.Scene.Border import Border
from  TankWarGame.Scene.IronWall import IronWall
from  TankWarGame.Scene.BrickWall import BrickWall
from  TankWarGame.Scene.Tree import Tree
from  TankWarGame.Scene.Home import Home
from  TankWarGame.Map.Map import Map
from  TankWarGame.Tank.Tank import Tank


'''
0: player0
1: player1
2: tree
3: brick wall
4: iron wall
5: home
6: none
'''

sence_dict = {
    2:Tree,
    3:BrickWall,
    4:IronWall,
    5:Home,
    6:Border,
}

class GameUI(QtWidgets.QFrame):
    def __init__(self, Form):
        super().__init__(Form)
        self.b_size = 24
        self.isfirst={0:True, 1:True}
        self.game_ui_width = 864
        self.game_ui_height = 672
        self.setGeometry( 0,  0, self.game_ui_width, self.game_ui_height)
        self.setStyleSheet('QWidget{background-color:black;}') 
        self.map_dict = Map(self.game_ui_width, self.game_ui_height, self.b_size).read_map()
        self.static_objs = dict()
        self.tank = {0:None, 1:None}
        self.generate_scene()

    def generate_scene(self):
        for dim in self.map_dict:
            if(self.map_dict[dim] == 7):
                continue
            if(self.map_dict[dim] == 0 and self.isfirst[0]):
                self.tank[0] = Tank(self, dim[0], dim[1], 0, 'right')
                self.isfirst[0] = False
            elif(self.map_dict[dim] == 1 and self.isfirst[1]):
                self.tank[1] = Tank(self, dim[0], dim[1], 1, 'left')
                self.isfirst[1] = False
            elif(self.map_dict[dim] != 0 and self.map_dict[dim] != 1):
                self.static_objs[dim] = sence_dict[self.map_dict[dim]](self, dim[0], dim[1])