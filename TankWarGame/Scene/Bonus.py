from TankWarGame.Scene.Tree import Tree
import random, time
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QThread
import math

class Bonus(QtWidgets.QPushButton):
    def __init__(self, game_ui):
        super().__init__(game_ui)       
        self.game_ui = game_ui
        self.game_info = game_ui.game_info
        self.life = True 
        self.bonus = self.game_info.bonus_obj
        self.show_time = 10
        self.freq = 30
        self.bonus_type = 0.1
    
    def random_xy(self):
        random.seed(time.time())
        self.x = random.randint(self.game_info.coord_left_x+1, self.game_info.coord_right_x-1)
        self.y = random.randint(self.game_info.coord_left_y+1, self.game_info.coord_right_y-1)

    def random_bonus(self):
        bonus_list = ['tank', 'star']
        bonus = random.choice(bonus_list)
        self.bonus_type = (bonus_list.index(bonus) + 1)/10
        return bonus

    def update_flag(self):
        self.game_info.map_dict[(self.x, self.y)] = self.game_info.bonus_type = self.bonus_type
        
    def clear_flag(self):
        self.game_info.map_dict[(self.x, self.y)] = self.game_info.bonus_type = self.game_info.none
        
    def show(self):
        self.life = True
        while True:
            self.random_xy()
            if self.game_info.map_dict[(self.x, self.y)] == self.game_info.none and \
                math.pow((self.x - self.game_info.tank_objs[0].cur_x), 2) + math.pow((self.y - self.game_info.tank_objs[0].cur_y), 2) > 2.5 and \
                math.pow((self.x - self.game_info.tank_objs[1].cur_x), 2) + math.pow((self.y - self.game_info.tank_objs[1].cur_y), 2) > 2.5:
                    self.setGeometry(self.x*self.game_info.bsize, self.y*self.game_info.bsize, 32, 32)
                    break

        self.setStyleSheet('QPushButton{border-image:url(./TankWarGame/Image/bonus/%s.png)}'%self.random_bonus())
        self.update_flag()
        self.setVisible(True)
        
    def dead(self):
        self.life = False
        self.clear_flag()
        self.setVisible(False)
        