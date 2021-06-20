import time
import random
import math
import json
from PyQt5 import QtCore

class BonusWorker(QtCore.QThread):
    start_bonus = QtCore.pyqtSignal(str)
    stop_bonus = QtCore.pyqtSignal(str)
    def __init__(self, game_info):
        super().__init__()
        self.game_info = game_info
        self.x = None
        self.y = None
        self.bonus_name = None
        self.bonus_id = None
        self.keep_running = True

    def terminate(self):
        self.keep_running = False

    def run(self):
        while self.keep_running:

            self.x, self.y = self.find_xy()
            self.bonus_name, self.bonus_id = self.random_bonus()
            
            
            command = 'show_bonus'
            params = {'priority': self.game_info.priority, 'x': self.x, 'y': self.y, 'bonus_name': self.bonus_name, 'bonus_id': self.bonus_id}
            command_params ={'command': command, 'parameters': params}
            self.start_bonus.emit(json.dumps(command_params))
            time.sleep(random.randint(6, 13)-3)
            time.sleep(3)

            command = 'clear_bonus'
            params = {'priority': self.game_info.priority}
            command_params ={'command': command, 'parameters': params}
            self.stop_bonus.emit(json.dumps(command_params))
            time.sleep(random.randint(3, 5))

    def find_xy(self):
        while True:
            x, y = self.random_xy()
            if self.game_info.map_dict[(x, y)] == self.game_info.none and \
                math.pow((x - self.game_info.tank_objs[0].cur_x), 2) + math.pow((y - self.game_info.tank_objs[0].cur_y), 2) > 2.5 and \
                math.pow((x - self.game_info.tank_objs[1].cur_x), 2) + math.pow((y - self.game_info.tank_objs[1].cur_y), 2) > 2.5:
                    
                    break
        return x, y           

    def random_xy(self):
        random.seed(time.time())
        x = random.randint(self.game_info.coord_left_x+1, self.game_info.coord_right_x-1)
        y = random.randint(self.game_info.coord_left_y+1, self.game_info.coord_right_y-1)
        return x, y

    def random_bonus(self):
        bonus_list = ['tank', 'star']
        bonus_name = random.choice(bonus_list)
        bonus_id = (bonus_list.index(bonus_name) + 1)/10
        return bonus_name, bonus_id