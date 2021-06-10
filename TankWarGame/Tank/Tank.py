import sys
import threading
import time

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QThread
from TankWarGame.Tank.Bullet import Bullet
from TankWarGame.Tank.BulletWorker import BulletWorker
# from Bullet import bullet
# from Global import quan_var
# from Worker import work_bullet

class Tank(QtWidgets.QPushButton):
    def __init__(self, game_ui, x, y, id, direction):
        super().__init__(game_ui)
        self.id = id
        self.init_x = x
        self.init_y = y
        self.cur_x = x        
        self.cur_y = y        
        self.game_ui = game_ui
        self.game_info = game_ui.game_info
        self.direction = direction    
        self.life = 1000
        self.attack = 5
        self.defense = 2
        self.tank_speed = 1
        self.bullet_speed = 1
        self.lock = threading.Lock()

        self.change_direction(direction)
        self.setGeometry(x*self.game_info.bsize, y*self.game_info.bsize, self.game_info.bsize*2, self.game_info.bsize*2)
    
    def change_direction(self, direction):
        self.direction = direction
        self.setStyleSheet('QPushButton{border-image:url(./TankWarGame/Image/tank/tank%s_%s.png);}' % (self.id, direction))
    
    def clear_position(self, flag = 7):
        self.lock.acquire(timeout=0.02)
        self.game_info.map_dict[(self.cur_x, self.cur_y)] = flag
        self.game_info.map_dict[(self.cur_x+1, self.cur_y)] = flag
        self.game_info.map_dict[(self.cur_x, self.cur_y+1)] = flag
        self.game_info.map_dict[(self.cur_x+1, self.cur_y+1)] = flag
        self.lock.release()

    def move(self, direction):
        self.change_direction(direction)

        obj_id = self.check_front(direction)

        if ( (obj_id[0] == 7 or obj_id[0] == 2) and (obj_id[1] == 7 or obj_id[1] == 2)):

            self.clear_position(flag = 7)  

            if(direction=='left'):
                self.cur_x -= self.tank_speed
            elif(direction == 'right'):
                self.cur_x += self.tank_speed
            elif(direction == 'up'):
                self.cur_y -= self.tank_speed
            elif(direction=='down'):
                self.cur_y += self.tank_speed    

            self.setGeometry(self.cur_x*self.game_info.bsize, self.cur_y*self.game_info.bsize, self.game_info.bsize*2, self.game_info.bsize*2)
            self.update_map_dict(self.cur_x, self.cur_y)  
            #  更新quan_var.mytank_dict列表
            # self.flag_mytank()

    def check_front(self, direction):
        '''
        return (id, id)
        '''
        obj_id = (7, 7)
        if(direction=='left'):
            obj_id = (self.game_info.map_dict[(self.cur_x-1, self.cur_y)], self.game_info.map_dict[(self.cur_x-1, self.cur_y+1)])
        elif(direction == 'right'):
            obj_id = (self.game_info.map_dict[(self.cur_x+2, self.cur_y)], self.game_info.map_dict[(self.cur_x+2, self.cur_y+1)])
        elif(direction == 'up'):            
            obj_id = (self.game_info.map_dict[(self.cur_x, self.cur_y-1)], self.game_info.map_dict[(self.cur_x+1, self.cur_y-1)])
        elif(direction=='down'):            
            obj_id = (self.game_info.map_dict[(self.cur_x, self.cur_y+2)], self.game_info.map_dict[(self.cur_x+1, self.cur_y+2)])
 
        return obj_id


    def update_map_dict(self, x, y):  
        self.lock.acquire(timeout=0.02)
        self.game_info.map_dict[(x, y)] = self.id
        self.game_info.map_dict[(x + 1, y)] = self.id
        self.game_info.map_dict[(x, y + 1)] = self.id
        self.game_info.map_dict[(x + 1, y + 1)] = self.id
        self.lock.release()
    
    
    def shoot(self): 
        if not self.game_info.bullet_life[self.id]:
            self.game_info.bullet_life[self.id] = True
            self.bullet = Bullet(self.game_ui, self)
            try:
                self.bullet_worker = BulletWorker(self.bullet)
                self.bullet_worker.done_singnal.connect(self.shoot_done)
                self.bullet_worker.start()
            except Exception as e:
                print(e,'发射子弹错误')

    def shoot_done(self):
        self.game_info.bullet_life[self.id] = False
