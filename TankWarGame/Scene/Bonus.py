from PyQt5 import QtWidgets


class Bonus(QtWidgets.QPushButton):
    def __init__(self, game_ui):
        super().__init__(game_ui)       
        self.game_ui = game_ui
        self.game_info = game_ui.game_info
        self.life = True 
        self.bonus_img = None
        self.show_time = 10
        self.freq = 30
        self.bonus_id = 0.1
        self.x = 0
        self.y = 0
        self.bonus_name = None    

    

    def update_flag(self):
        self.game_info.map_dict[(self.x, self.y)] = self.game_info.bonus_id = self.bonus_id
        
    def clear_flag(self):
        self.game_info.map_dict[(self.x, self.y)] = self.game_info.bonus_id = self.game_info.none
        
    def show(self, x, y, bonus_name, bonus_id):
        self.life = True
        self.x = x
        self.y = y
        self.bonus_id = bonus_id
        self.setGeometry(self.x * self.game_info.bsize, self.y * self.game_info.bsize, 32, 32)
        self.setStyleSheet('QPushButton{border-image:url(./TankWarGame/Image/bonus/%s.png)}' % bonus_name)
        self.update_flag()
        self.setVisible(True)
    
    def dead(self):
        self.life = False
        self.clear_flag()
        self.setVisible(False)
        