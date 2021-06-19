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
        self.dead_flag = False
        self.bullet_life = False
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
        if (self.dead_flag != True and (self.game_info.game_over != True)):
            
            self.change_direction(direction)
            obj_id = self.check_front(direction)
            print(obj_id)

            if ( (obj_id[0] == self.game_info.none or obj_id[0] == self.game_info.tree or obj_id[0] == self.game_info.bonus_tank or obj_id[0] == self.game_info.bonus_star) \
                and (obj_id[1] == self.game_info.none or obj_id[1] == self.game_info.tree or obj_id[1] == self.game_info.bonus_tank or obj_id[1] == self.game_info.bonus_star)):

                self.clear_position()
                
                if self.game_info.bonus_tank in obj_id:
                    self.game_info.bonus_obj.dead()
                    self.game_info.bullet_level = 2
                    self.game_info.bouns_music.play()
                    print('Got Bonus: tank')
                elif self.game_info.bonus_star in obj_id:
                    self.game_info.bonus_obj.dead()
                    self.beHit(self.ATK*(-1))
                    self.game_info.bouns_music.play()
                    print(f'Got Bonus: star, {self.game_info.tank_hp}')

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
        if ((self.dead_flag != True) and (not self.bullet_life) and (self.game_info.game_over != True)):
            self.bullet_life = True
            self.bullet = Bullet(self.game_ui, self)
            try:
                self.bullet_worker = BulletWorker(self.bullet)
                self.bullet_worker.done_singnal.connect(self.shoot_done)
                self.bullet_worker.start()
            except Exception as e:
                print(e,'shoot error')

    def shoot_done(self):
        self.bullet_life = False

    def beHit(self, ATK):
        self.HP -= ATK
        if self.HP > 100:
            self.HP = 100
        self.game_info.stat_ui.update_tank_hp(self.id, self.HP)
        QtWidgets.QApplication.processEvents()
        if(self.HP <= 0):
            self.dead()

    def dead(self):
        self.setVisible(False)
        self.clear_position()
        self.dead_flag = True
        threading.Timer(self.game_info.rebirth_time, self.rebirth).start()

    def rebirth(self):
        self.cur_x, self.cur_y = self.rebirth_pos(self.init_x, self.init_y)
        self.setGeometry(self.cur_x*self.game_info.bsize, self.cur_y*self.game_info.bsize, self.game_info.bsize*2, self.game_info.bsize*2)
        self.update_map_dict(self.cur_x, self.cur_y)
        self.HP = self.game_info.tank_hp
        self.game_info.stat_ui.update_tank_hp(self.id, self.HP)
        self.setVisible(True)
        self.dead_flag = False
        QtWidgets.QApplication.processEvents()

    def rebirth_pos(self, init_x, init_y):
        while (self.game_info.map_dict[(init_x, init_y)] != self.game_info.none and 
            self.game_info.map_dict[(init_x+1, init_y)] != self.game_info.none and 
            self.game_info.map_dict[(init_x, init_y+1)] != self.game_info.none and 
            self.game_info.map_dict[(init_x+1, init_y+1)] != self.game_info.none):
            init_y -= 1
            print(init_y)
        return init_x, init_y
            