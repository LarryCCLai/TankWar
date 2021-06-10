from PyQt5 import QtWidgets, QtGui, QtCore
from  TankWarGame.Tank.Tank import Tank
from  TankWarGame.Scene.Tree import Tree
from  TankWarGame.Scene.BrickWall import BrickWall
from  TankWarGame.Scene.IronWall import IronWall
from  TankWarGame.Scene.Home import Home
from TankWarGame.Scene.Border import Border
from  TankWarGame.Map.Map import Map

sence_dict = {
    2:Tree,
    3:BrickWall,
    4:IronWall,
    5:Home,
    6:Border,
}

class GameUI(QtWidgets.QFrame):
    def __init__(self, Form, game_info):
        super().__init__(Form)
        self.game_info = game_info
        self.setGeometry( 0,  0, self.game_info.game_ui_width, self.game_info.game_ui_height)
        # self.setStyleSheet('QWidget{background-color:black;}') 
        self.tank = {0:None, 1:None}
        self.generate_scene()

    def generate_scene(self):
        isfirst = {0:True, 1:True}
        for coord in self.game_info.map_dict:
            if(self.game_info.map_dict[coord] == self.game_info.none ):
                continue
            if(self.game_info.map_dict[coord] == self.game_info.tree):
                self.game_info.static_objs[coord].setGeometry(coord[0]*self.game_info.bsize,coord[1]*self.game_info.bsize,self.game_info.bsize,self.game_info.bsize)
                
            if(self.game_info.map_dict[coord] == self.game_info.tank0 and isfirst[0]):
                self.tank[0] = Tank(self, coord[0], coord[1], 0, 'right')
                isfirst[0] = False

            elif(self.game_info.map_dict[coord] == self.game_info.tank1 and isfirst[1]):
                self.tank[1] = Tank(self, coord[0], coord[1], 1, 'left')
                isfirst[1] = False

            elif(self.game_info.map_dict[coord] != self.game_info.tank0 and self.game_info.map_dict[coord] != self.game_info.tank1):
                self.game_info.static_objs[coord] = sence_dict[self.game_info.map_dict[coord]](self, coord[0], coord[1])