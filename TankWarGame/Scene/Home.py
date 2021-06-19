from PyQt5 import QtWidgets, QtCore, QtGui

class Home(QtWidgets.QPushButton):
    def __init__(self, game_ui, x, y):
        super().__init__(game_ui)
        self.game_ui = game_ui
        self.game_info = game_ui.game_info
        self.HP = self.game_info.home_hp
        
        self.setText('')
        self.setStyleSheet('QPushButton{border-image:url(./TankWarGame/Image/scene/home1.png);}')
        self.setGeometry(x*self.game_info.bsize, y*self.game_info.bsize, self.game_info.bsize*2, self.game_info.bsize*2)            
        self.setEnabled(False)
    

    def beHit(self, id, ATK):
        self.HP -= ATK
        self.game_info.stat_ui.update_home_hp(id, self.HP)
        QtWidgets.QApplication.processEvents()
        if(self.HP <= 0):
            self.dead(id)
    
        
    def dead(self, id):
        print('[Home.py->dead] GameOver')

        if(id == self.game_info.tank0):
            print('player {} win, player {} loss'.format(self.game_info.tank1, self.game_info.tank0))
            self.game_info.stat_ui.update_result(self.game_info.tank1)
            self.game_info.winner = self.game_info.tank1
            self.game_info.loser = self.game_info.tank0
        else:
            print('player {} win, player {} loss'.format(self.game_info.tank0, self.game_info.tank1))
            self.game_info.stat_ui.update_result(self.game_info.tank0)
            self.game_info.winner = self.game_info.tank0
            self.game_info.loser = self.game_info.tank1

        self.game_info.game_over = True
        self.game_ui.game_over.setChecked(True)
        
        

        
        # process