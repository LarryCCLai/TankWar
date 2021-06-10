from PyQt5 import QtWidgets, QtGui, QtCore
from  TankWarGame.Tank.Tank import Tank
from  TankWarGame.Scene.Tree import Tree
from  TankWarGame.Scene.BrickWall import BrickWall
from  TankWarGame.Scene.IronWall import IronWall
from  TankWarGame.Scene.Home import Home
from TankWarGame.Scene.Border import Border
from  TankWarGame.Map.Map import Map


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
    def __init__(self, Form, game_info):
        super().__init__(Form)
        self.game_info = game_info
        self.setGeometry( 0,  0, self.game_info.game_ui_width, self.game_info.game_ui_height)
        # self.setStyleSheet('QWidget{background-color:black;}') 
        self.tank = {0:None, 1:None}
        self.generate_scene()

    def generate_scene(self):
        isfirst = {0:True, 1:True}
        for dim in self.game_info.map_dict:
            if(self.game_info.map_dict[dim] == self.game_info.none ):
                continue
            if(self.game_info.map_dict[dim] == self.game_info.tree):
                self.game_info.static_objs[dim].setGeometry(dim[0]*self.game_info.bsize,dim[1]*self.game_info.bsize,self.game_info.bsize,self.game_info.bsize)
# or self.game_info.map_dict[dim] == self.game_info.tree
            if(self.game_info.map_dict[dim] == self.game_info.tank0 and isfirst[0]):
                self.tank[0] = Tank(self, dim[0], dim[1], 0, 'right')
                isfirst[0] = False

            elif(self.game_info.map_dict[dim] == self.game_info.tank1 and isfirst[1]):
                self.tank[1] = Tank(self, dim[0], dim[1], 1, 'left')
                isfirst[1] = False

            elif(self.game_info.map_dict[dim] != self.game_info.tank0 and self.game_info.map_dict[dim] != self.game_info.tank1):
                self.game_info.static_objs[dim] = sence_dict[self.game_info.map_dict[dim]](self, dim[0], dim[1])