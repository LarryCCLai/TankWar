from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QThread
from  TankWarGame.Tank.Tank import Tank
from  TankWarGame.Scene.Tree import Tree
from  TankWarGame.Scene.BrickWall import BrickWall
from  TankWarGame.Scene.IronWall import IronWall
from  TankWarGame.Scene.Home import Home
from TankWarGame.Scene.Border import Border
from  TankWarGame.Map.Map import Map
from TankWarGame.Scene.Bonus import Bonus
sence_dict = {
    2:Tree,
    3:BrickWall,
    4:IronWall,
    6:Border,
}

class GameUI(QtWidgets.QFrame):
    def __init__(self, Form, game_info):
        super().__init__(Form)
        self.game_info = game_info
        self.setGeometry( 0,  0, self.game_info.game_ui_width, self.game_info.game_ui_height)
        self.setStyleSheet('QWidget{background-color:black;}') 
        self.tank = {0:None, 1:None}
        self.home = {0:None, 1:None}
        self.game_over = QtWidgets.QCheckBox('Gameover.')
        self.game_over.setChecked(False)
        self.generate_home()
        self.generate_tank()
        self.generate_scene()
        self.bonus_init()
        print(self.game_info.tank_objs)
    def generate_home(self):
        home_isfirst = {0:True, 1:True}
        for coord in self.game_info.map_dict:
            if(self.game_info.map_dict[coord] != self.game_info.home0 and 
                self.game_info.map_dict[coord] != self.game_info.home1):
                continue
            if(coord[0]< 15 and home_isfirst[0] and self.game_info.map_dict[coord] == self.game_info.home0):
                self.game_info.home_objs[0] = Home(self, coord[0], coord[1])
                self.game_info.static_objs[(coord[0], coord[1])] = self.game_info.home_objs[0] 
                self.game_info.static_objs[(coord[0]+1, coord[1])] = self.game_info.home_objs[0] 
                self.game_info.static_objs[(coord[0], coord[1]+1)] = self.game_info.home_objs[0] 
                self.game_info.static_objs[(coord[0]+1, coord[1]+1)] = self.game_info.home_objs[0] 
                home_isfirst[0] = False
            elif(coord[0] > 15 and home_isfirst[1] and self.game_info.map_dict[coord] == self.game_info.home1):
                self.game_info.home_objs[1] = Home(self, coord[0], coord[1])
                self.game_info.static_objs[(coord[0], coord[1])] = self.game_info.home_objs[1]
                self.game_info.static_objs[(coord[0]+1, coord[1])] = self.game_info.home_objs[1]
                self.game_info.static_objs[(coord[0], coord[1]+1)] = self.game_info.home_objs[1]
                self.game_info.static_objs[(coord[0]+1, coord[1]+1)] = self.game_info.home_objs[1]
                home_isfirst[1] = False
            if(home_isfirst[0] == False and home_isfirst[1] == False):
                break

    def generate_tank(self):
        isfirst = {0:True, 1:True}
        for coord in self.game_info.map_dict:
            if(self.game_info.map_dict[coord] != self.game_info.tank0 and 
                self.game_info.map_dict[coord] != self.game_info.tank1):
                continue

            if(self.game_info.map_dict[coord] == self.game_info.tank0 and isfirst[0]):
                    self.game_info.tank_objs[0] = Tank(self, coord[0], coord[1], 0, 'right')
                    isfirst[0] = False

            elif(self.game_info.map_dict[coord] == self.game_info.tank1 and isfirst[1]):
                self.game_info.tank_objs[1] = Tank(self, coord[0], coord[1], 1, 'left')
                isfirst[1] = False   
            if(isfirst[0] == False and isfirst[1] == False):
                break
    
    def generate_scene(self):
        for coord in self.game_info.map_dict:
            if(self.game_info.map_dict[coord] == self.game_info.none or
                self.game_info.map_dict[coord] == self.game_info.tank0 or 
                self.game_info.map_dict[coord] == self.game_info.tank1 or
                self.game_info.map_dict[coord] == self.game_info.home or
                self.game_info.map_dict[coord] == self.game_info.home0 or
                self.game_info.map_dict[coord] == self.game_info.home1):
                continue
            self.game_info.static_objs[coord] = sence_dict[self.game_info.map_dict[coord]](self, coord[0], coord[1])
    
    def bonus_init(self):
        self.game_info.bonus_obj = Bonus(self)
        