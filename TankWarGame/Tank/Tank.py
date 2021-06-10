import sys
import threading
import time

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QThread
from TankWarGame.Tank.Bullet import Bullet
from TankWarGame.Tank.BulletWorker import BulletWorker

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
        self.HP = self.game_info.tank_hp
        self.ATK = self.game_info.tank_atk
        self.speed = self.game_info.tank_speed
        self.lock = threading.Lock()

        self.change_direction(direction)
        self.setGeometry(x*self.game_info.bsize, y*self.game_info.bsize, self.game_info.bsize*2, self.game_info.bsize*2)
        self.setEnabled(False)

    def change_direction(self, direction):
        self.direction = direction
        self.setStyleSheet('QPushButton{border-image:url(./TankWarGame/Image/tank/tank%s_%s.png);}' % (self.id, direction))
    
    def clear_position(self):
        self.lock.acquire(timeout=0.02)
        self.game_info.map_dict[(self.cur_x, self.cur_y)] = self.game_info.none
        self.game_info.map_dict[(self.cur_x+1, self.cur_y)] = self.game_info.none
        self.game_info.map_dict[(self.cur_x, self.cur_y+1)] = self.game_info.none
        self.game_info.map_dict[(self.cur_x+1, self.cur_y+1)] = self.game_info.none
        self.lock.release()

    def move(self, direction):
        self.change_direction(direction)

        obj_id = self.check_front(direction)

        if ( (obj_id[0] == self.game_info.none or obj_id[0] == self.game_info.tree) and (obj_id[1] == self.game_info.none or obj_id[1] == self.game_info.tree)):

            self.clear_position()  

            if(direction=='left'):
                self.cur_x -= self.speed
            elif(direction == 'right'):
                self.cur_x += self.speed
            elif(direction == 'up'):
                self.cur_y -= self.speed
            elif(direction=='down'):
                self.cur_y += self.speed    

            self.setGeometry(self.cur_x*self.game_info.bsize, self.cur_y*self.game_info.bsize, self.game_info.bsize*2, self.game_info.bsize*2)
            self.update_map_dict(self.cur_x, self.cur_y)  

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
                print(e,'shoot error')

    def shoot_done(self):
        self.game_info.bullet_life[self.id] = False
