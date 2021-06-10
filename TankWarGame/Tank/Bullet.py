import time
import sys

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QThread
# print(front_info)
#         print('tank:', self.tank_obj.cur_x, self.tank_obj.cur_y)
#         print(left_dim)
#         print(right_dim)
#         print(self.game_info.map_dict[left_dim])
#         print(self.game_info.map_dict[right_dim])
class Bullet(QtWidgets.QPushButton):
    def __init__(self, game_ui, tank_obj):
        super().__init__(game_ui)
        self.tank_obj = tank_obj               
        self.direction = tank_obj.direction   
        self.game_ui = game_ui
        self.game_info = game_ui.game_info                   
        self.life = True                     
        self.speed = 12

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
        left_dim = (front_info[1][0])//24, (front_info[1][1])//24
        right_dim =(front_info[2][0])//24, (front_info[2][1])//24
        
        self.game_info.map_dict[left_dim] = self.game_info.none
        self.game_info.map_dict[right_dim] = self.game_info.none

        self.game_info.static_objs[left_dim].setVisible(False)
        self.game_info.static_objs[right_dim].setVisible(False)
        

    def destroy_left(self, front_info):
        left_dim = (front_info[1][0])//24, (front_info[1][1])//24
        self.game_info.map_dict[left_dim] = self.game_info.none
        self.game_info.static_objs[left_dim].setVisible(False)
        

    def destroy_right(self, front_info):
        right_dim =(front_info[2][0])//24, (front_info[2][1])//24
        self.game_info.map_dict[right_dim] = self.game_info.none
        self.game_info.static_objs[right_dim].setVisible(False)
        

    def move(self):
        '''
        front_info = ((front left id, front right id), front left dim, front right dim)
        '''
        front_info = self.check_front()
        if front_info[0] == (self.game_info.tank0, self.game_info.tank0):
            self.dead()  
            # TO-DO
        elif front_info[0] == (self.game_info.tank1, self.game_info.tank1):
            self.dead()  
            # TO-DO
        elif front_info[0] == (self.game_info.home, self.game_info.home):  
            self.dead()   
            # TO-DO 
        elif front_info[0] == (self.game_info.brick_wall, self.game_info.home):  
            self.destroy_left(front_info)
            self.dead()   
            # TO-DO  
        elif front_info[0] == (self.game_info.home, self.game_info.brick_wall):  
            self.destroy_right(front_info)
            self.dead()  
            # TO-DO 

        elif front_info[0] == (self.game_info.border, self.game_info.border):
            self.dead()
        elif ((front_info[0][0] == self.game_info.tank0 or front_info[0][0] == self.game_info.tank1) and 
                front_info[0][1] != self.game_info.tank0 and front_info[0][1] != self.game_info.tank1 and 
                front_info[0][1] != self.game_info.none):
            self.destroy_left(front_info)
            self.dead() 
        elif ((front_info[0][1] == self.game_info.tank0 or front_info[0][1] == self.game_info.tank1) and 
                front_info[0][0] != self.game_info.tank0 and front_info[0][0] != self.game_info.tank1 and
                front_info[0][0] != self.game_info.none):
            self.destroy_left(front_info)
            self.dead()

        elif front_info[0] == (self.game_info.brick_wall, self.game_info.brick_wall):
            self.destroy_all(front_info)
            self.dead()
        elif front_info[0] == (self.game_info.brick_wall, self.game_info.none):  
            self.destroy_left(front_info)
            self.dead()     
        elif front_info[0] == (self.game_info.none, self.game_info.brick_wall):  
            self.destroy_right(front_info)
            self.dead()
        elif front_info[0] == (self.game_info.brick_wall, self.game_info.tree):  
            self.destroy_left(front_info)
            self.dead() 
        elif front_info[0] == (self.game_info.tree, self.game_info.brick_wall):  
            self.destroy_right(front_info)
            self.dead() 
        
        elif front_info[0] == (self.game_info.iron_wall, self.game_info.iron_wall):
            self.dead()
        elif front_info[0] == (self.game_info.iron_wall, self.game_info.none):  
            self.dead()    
        elif front_info[0] == (self.game_info.none, self.game_info.iron_wall):  
            self.dead()
        elif front_info[0] == (self.game_info.iron_wall, self.game_info.tree):  
            self.dead()
        elif front_info[0] == (self.game_info.tree, self.game_info.iron_wall):      
            self.dead()
        
        elif front_info[0] == (self.game_info.brick_wall, self.game_info.iron_wall):  
            self.destroy_left(front_info)
            self.dead()
        elif front_info[0] == (self.game_info.iron_wall, self.game_info.brick_wall):  
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
            ((front left id, front right id), front left dim, front right dim)
        '''
        left_dim = None
        right_dim = None
        lr_id = None
        if (self.direction == 'down'): 
            left_dim = (self.x-18, self.y + self.speed)
            right_dim = (self.x+6, self.y + self.speed)
            lr_id = (self.game_info.map_dict.get(((self.x-18)//24, (self.y+self.speed)//24), self.game_info.none), 
                    self.game_info.map_dict.get(((self.x+6)//24, (self.y + self.speed)//24), self.game_info.none))
            
        elif (self.direction == 'up'): 
            left_dim = (self.x-18, self.y - self.speed)
            right_dim = (self.x +6, self.y -self.speed)
            lr_id = (self.game_info.map_dict.get(((self.x-18)//24, (self.y - self.speed)//24), self.game_info.none), 
                    self.game_info.map_dict.get(((self.x+6)//24, (self.y -self.speed)//24), self.game_info.none))

        elif (self.direction == 'right'):  
            left_dim = (self.x + self.speed, self.y-18)
            right_dim = (self.x + self.speed, self.y+6)
            lr_id = (self.game_info.map_dict.get(((self.x +self.speed)//24, (self.y -18)//24), self.game_info.none), 
                    self.game_info.map_dict.get(((self.x +self.speed)//24, (self.y+6)//24), self.game_info.none))

        elif (self.direction == 'left'):  
            left_dim = (self.x-self.speed,self.y-18)
            right_dim = (self.x-self.speed,self.y+6)
            lr_id = (self.game_info.map_dict.get(((self.x-self.speed)//24,(self.y-18)//24), self.game_info.none), 
                    self.game_info.map_dict.get(((self.x-self.speed)//24,(self.y+6)//24), self.game_info.none))
        return (lr_id, left_dim, right_dim)

    def dead(self):
        self.game_info.bullet_music.play()
        self.setGeometry(self.x - 18, self.y - 18, 48, 48)
        self.setStyleSheet('QPushButton{border-image:url(./TankWarGame/Image/others/boom_static.png)}')
        time.sleep(0.025)
        self.setVisible(False)
        QtWidgets.QApplication.processEvents()
        self.life = False
        
