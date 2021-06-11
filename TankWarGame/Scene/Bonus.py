from TankWarGame.Scene.Tree import Tree
import random

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QThread

class Bonus(QtWidgets.QPushButton):
    def __init__(self, game_ui, Form):
        super().__init__(game_ui)       
        self.game_ui = game_ui
        self.game_info = game_ui.game_info
        self.life = True 
        self.bonus = self.game_info.bonus_obj
        self.show_time = 10
        self.freq = 30
        self.bonus_type = 0.1
        self.form = Form
    
    def random_xy(self):
        self.x = random.randint(0, 25)
        self.y = random.randint(0, 25)
        return self.x * 24 + 24, self.y * 24 + 24

    def random_bonus(self):
        foods = ['tank', 'tank', 'tank']
        food = random.choice(foods)
        self.food_type = (foods.index(food) + 1)/10
        return food

    def update_flag(self):
        if self.game_info.map_dict.get((self.x, self.y), 0) <= 1:
            self.game_info.map_dict[(self.x, self.y)] = self.food_type
        if self.game_info.map_dict.get((self.x + 1, self.y), 0) <= 1:
            self.game_info.map_dict[(self.x + 1, self.y)] = self.food_type
        if self.game_info.map_dict.get((self.x, self.y + 1), 0) <= 1:
            self.game_info.map_dict[(self.x, self.y + 1)] = self.food_type
        if self.game_info.map_dict.get((self.x + 1, self.y + 1), 0) <= 1:
            self.game_info.map_dict[(self.x + 1, self.y + 1)] = self.food_type

    def clear_flag(self):
        if self.game_info.map_dict.get((self.x, self.y), 0) < 1:
            self.game_info.map_dict[(self.x, self.y)] = 0
        if self.game_info.map_dict.get((self.x + 1, self.y), 0) < 1:
            self.game_info.map_dict[(self.x + 1, self.y)] = 0
        if self.game_info.map_dict.get((self.x, self.y + 1), 0) < 1:
            self.game_info.map_dict[(self.x, self.y + 1)] = 0
        if self.game_info.map_dict.get((self.x + 1, self.y + 1), 0) < 1:
            self.game_info.map_dict[(self.x + 1, self.y + 1)] = 0
    
    def set_bonus_range(self):
        self.game_info.bonus_dict = {}
        self.game_info.bonus_dict[(self.x * 24 + 24, self.y * 24 + 24)] = self
        self.game_info.bonus_dict[(self.x * 24 + 48, self.y * 24 + 24)] = self
        self.game_info.bonus_dict[(self.x * 24 + 24, self.y * 24 + 48)] = self
        self.game_info.bonus_dict[(self.x * 24 + 48, self.y * 24 + 48)] = self
        
    def show_bonus(self):
        self.life = True
        self.food_icon = QtWidgets.QPushButton(self.form)
        while True:
            x, y = self.random_xy()
            if not (self.game_info.map_dict.get((self.x, self.y), 0) and self.game_info.map_dict.get((self.x + 1, self.y), 0) and\
                self.game_info.map_dict.get((self.x, self.y + 1), 0) and self.game_info.map_dict.get((self.x + 1, self.y + 1), 0)):
                self.food_icon.setGeometry(x, y, 44, 44)
                break
        self.food_icon.setStyleSheet('QPushButton{border-image:url(./TankWarGame/Image/bonus/food_%s.png)}'%self.random_bonus())
        self.update_flag()
        self.food_icon.setVisible(True)
        
    def dead(self):
        self.life = False
        self.clear_flag()
        self.food_icon.setVisible(False)
        