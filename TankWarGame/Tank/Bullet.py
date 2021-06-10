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
        self.speed = 12

        self.x, self.y = self.xy_(self.tank_obj.cur_x,self.tank_obj.cur_y)                           
        self.setGeometry(self.x, self.y, 12, 12)
        self.setStyleSheet('QPushButton{border-image:url(./TankWarGame/Image/bullet/bullet_%s.png)}' % (self.direction))
        self.setVisible(True)

    def xy_(self, cur_x, cur_y):
        x = cur_x * self.game_info.bsize
        y = cur_y * self.game_info.bsize
        if self.direction == 'up':
            x = x + 18
            y = y - 12
        elif self.direction == 'down':
            x = x + 18
            y = y + 48
        elif self.direction == 'left':
            x = x - 12
            y = y + 18
        elif self.direction == 'right':
            x = x + 48
            y = y + 18
        return x, y

    def move(self):
        # 得到子弹前方的物体类型
        front_info = self.check_front()

        if front_info[0] == (self.game_info.brick_wall, self.game_info.brick_wall):
            try:
                left_dim = (front_info[1][0] - 24)//24, (front_info[1][1] - 24)//24
                right_dim =(front_info[2][0] - 24)//24, (front_info[2][1]-24)//24

                self.game_info.map_dict[left_dim] = self.game_info.none
                self.game_info.map_dict[right_dim] = self.game_info.none

                self.game_info.static_obj[left_dim].setVisible(False)
                self.game_info.static_obj[right_dim].setVisible(False)
                self.game_info.bullet_music.play()
                self.dead()
            except Exception as e:
                print('击中土砖错误',e)
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
            [(front left id, front right id), front left dim, front right dim]
        '''
        left_dim = None
        right_dim = None
        lr_id = None
        if (self.direction == 'down'): 
            left_dim = (self.x-18, self.y + self.speed)
            right_dim = (self.x+6, self.y + self.speed)
            lr_id = (self.game_info.map_dict.get(((self.x-18-24)//24, (self.y+self.speed-24)//24), self.game_info.none), 
                    self.game_info.map_dict.get(((self.x+6-24)//24, (self.y + self.speed-24)//24), self.game_info.none))
            
        elif (self.direction == 'up'): 
            left_dim = (self.x-18, self.y - self.speed)
            right_dim = (self.x +6, self.y -self.speed)
            lr_id = (self.game_info.map_dict.get(((self.x-42)//24, (self.y - self.speed-24)//24), self.game_info.none), 
                    self.game_info.map_dict.get(((self.x-18)//24, (self.y -self.speed-24)//24), self.game_info.none))

        elif (self.direction == 'right'):  
            left_dim = (self.x + self.speed, self.y-18)
            right_dim = (self.x + self.speed, self.y+6)
            lr_id = (self.game_info.map_dict.get(((self.x +self.speed-24)//24, (self.y -18-24)//24), self.game_info.none), 
                    self.game_info.map_dict.get(((self.x +self.speed-24)//24, (self.y+6-24)//24), self.game_info.none))

        elif (self.direction == 'left'):  
            left_dim = (self.x-self.speed,self.y-18)
            right_dim = (self.x-self.speed,self.y+6)
            lr_id = (self.game_info.map_dict.get(((self.x-self.speed-24)//24,(self.y-18-24)//24), self.game_info.none), 
                    self.game_info.map_dict.get(((self.x-self.speed-24)//24,(self.y+6-24)//24), self.game_info.none))
        return (lr_id, left_dim, right_dim)

    def dead(self):
        self.setGeometry(self.x - 18, self.y - 18, 48, 48)
        self.setStyleSheet('QPushButton{border-image:url(./TankWarGame/Image/others/boom_static.png)}')
        QtWidgets.QApplication.processEvents()
        time.sleep(0.025)
        self.life = False
        self.setVisible(False)

