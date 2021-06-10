from TankWarGame.Scene.Tree import Tree
import time
import sys

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QThread

class Bullet(QtWidgets.QPushButton):
    def __init__(self, game_ui, tank_obj):
        super().__init__(game_ui)
        self.tank_obj = tank_obj               
        self.direction = tank_obj.direction   
        self.game_ui = game_ui
        self.game_info = game_ui.game_info                   
        self.life = True                     
        self.speed = self.game_info.bullet_speed

        self.x, self.y = self.xy_(self.tank_obj.cur_x,self.tank_obj.cur_y)                           
        self.setGeometry(self.x, self.y, 12, 12)
        self.setStyleSheet('QPushButton{border-image:url(./TankWarGame/Image/bullet/bullet_%s.png)}' % (self.direction))
        self.setVisible(True)

    def xy_(self, cur_x, cur_y):
        x = cur_x * self.game_info.bsize
        y = cur_y * self.game_info.bsize

        if self.direction == 'left':
            x = x - 12
            y = y + 18
        elif self.direction == 'right':
            x = x + 48
            y = y + 18
        elif self.direction == 'up':
            x = x + 18
            y = y - 12
        elif self.direction == 'down':
            x = x + 18
            y = y + 48
        
        return x, y

    def destroy_all(self, front_info):
        left_coord = (front_info[1][0])//self.game_info.bsize, (front_info[1][1])//self.game_info.bsize
        right_coord =(front_info[2][0])//self.game_info.bsize, (front_info[2][1])//self.game_info.bsize
        
        self.game_info.map_dict[left_coord] = self.game_info.none
        self.game_info.map_dict[right_coord] = self.game_info.none

        self.game_info.static_objs[left_coord].setVisible(False)
        self.game_info.static_objs[right_coord].setVisible(False)
        

    def destroy_left(self, front_info):
        left_coord = (front_info[1][0])//self.game_info.bsize, (front_info[1][1])//self.game_info.bsize
        self.game_info.map_dict[left_coord] = self.game_info.none
        self.game_info.static_objs[left_coord].setVisible(False)
        

    def destroy_right(self, front_info):
        right_coord =(front_info[2][0])//self.game_info.bsize, (front_info[2][1])//self.game_info.bsize
        self.game_info.map_dict[right_coord] = self.game_info.none
        self.game_info.static_objs[right_coord].setVisible(False)
    
    def move(self):
        '''
        front_info = ((front left id, front right id), front left coord, front right coord)
        '''
        front_info = self.check_front()
        elementR = front_info[0][1]
        elementL = front_info[0][0]
        if elementL == self.game_info.brick_wall  or elementL == self.game_info.iron_wall or elementL == self.game_info.border or elementL == self.game_info.home:
            if elementL == self.game_info.brick_wall or elementL == self.game_info.home: 
                self.destroy_left(front_info)
            self.dead()
        elif elementR == self.game_info.brick_wall  or elementR == self.game_info.iron_wall or elementR == self.game_info.border or elementR == self.game_info.home:
            if elementR == self.game_info.brick_wall or elementR == self.game_info.home: 
                self.destroy_right(front_info)
            self.dead()
        else:
            if(self.direction == 'left'):
                self.x = self.x - self.speed        
            if(self.direction == 'right'):
                self.x = self.x + self.speed    
            if(self.direction == 'up'):
                self.y = self.y - self.speed    
            if(self.direction == 'down'):
                self.y = self.y + self.speed
            self.setGeometry(self.x, self.y, 12, 12)
            self.setVisible(True)

    def check_front(self):
        '''
            ((front left id, front right id), front left coord, front right coord)
        '''
        left_coord = None
        right_coord = None
        lr_id = None
        if (self.direction == 'down'): 
            left_coord = (self.x-18, self.y + self.speed)
            right_coord = (self.x+6, self.y + self.speed)
            lr_id = (self.game_info.map_dict.get(((self.x-18)//self.game_info.bsize, (self.y+self.speed)//self.game_info.bsize), self.game_info.none), 
                    self.game_info.map_dict.get(((self.x+6)//self.game_info.bsize, (self.y + self.speed)//self.game_info.bsize), self.game_info.none))
            
        elif (self.direction == 'up'): 
            left_coord = (self.x-18, self.y - self.speed)
            right_coord = (self.x +6, self.y -self.speed)
            lr_id = (self.game_info.map_dict.get(((self.x-18)//self.game_info.bsize, (self.y - self.speed)//self.game_info.bsize), self.game_info.none), 
                    self.game_info.map_dict.get(((self.x+6)//self.game_info.bsize, (self.y -self.speed)//self.game_info.bsize), self.game_info.none))

        elif (self.direction == 'right'):  
            left_coord = (self.x + self.speed, self.y-18)
            right_coord = (self.x + self.speed, self.y+6)
            lr_id = (self.game_info.map_dict.get(((self.x +self.speed)//self.game_info.bsize, (self.y -18)//self.game_info.bsize), self.game_info.none), 
                    self.game_info.map_dict.get(((self.x +self.speed)//self.game_info.bsize, (self.y+6)//self.game_info.bsize), self.game_info.none))

        elif (self.direction == 'left'):  
            left_coord = (self.x-self.speed,self.y-18)
            right_coord = (self.x-self.speed,self.y+6)
            lr_id = (self.game_info.map_dict.get(((self.x-self.speed)//self.game_info.bsize,(self.y-18)//self.game_info.bsize), self.game_info.none), 
                    self.game_info.map_dict.get(((self.x-self.speed)//self.game_info.bsize,(self.y+6)//self.game_info.bsize), self.game_info.none))
        return (lr_id, left_coord, right_coord)

    def dead(self):
        self.game_info.bullet_music.play()
        self.setGeometry(self.x - 18, self.y - 18, 48, 48)
        self.setStyleSheet('QPushButton{border-image:url(./TankWarGame/Image/others/boom_static.png)}')
        time.sleep(0.025)
        self.setVisible(False)
        QtWidgets.QApplication.processEvents()
        self.life = False
        
