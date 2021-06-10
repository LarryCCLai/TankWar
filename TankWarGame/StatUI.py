from PyQt5 import QtWidgets, QtGui, QtCore

color = {0:'yellow', 1:'green'}
icon = {0:'QPushButton{border-image:url(./TankWarGame/Image/tank/tank0_up.png);}',
        1:'QPushButton{border-image:url(./TankWarGame/Image/tank/tank1_up.png);}',}

class StatLabel(QtWidgets.QLabel):
    def __init__(self, Form, rect, content, font_size, color='black'):
        super().__init__(Form)
        self.setGeometry(rect)
        self.setWordWrap(True)
        self.setFont(QtGui.QFont('微軟正黑體', font_size, QtGui.QFont.Bold))
        self.setStyleSheet('color:{}'.format(color))
        self.setText(content)
class Icon(QtWidgets.QPushButton):
    def __init__(self, Form, rect, image):
        super().__init__(Form)
        self.setGeometry(rect)
        self.setStyleSheet(image)

class PlayerInfo(QtWidgets.QFrame):
    def __init__(self, Form, rect, id):
        super().__init__(Form)
        self.setGeometry(rect)
        self.tank_icon = Icon(self, QtCore.QRect(10, 10, 36, 36), icon[id])
        self.player_header = StatLabel(self, QtCore.QRect(10, 50, 200, 20), 'Player {} Info.'.format(id), 13 , color[id])
        self.name = StatLabel(self, QtCore.QRect(10, 75, 200, 20), 'Name: None', 13 , color[id])
        self.tank_header = StatLabel(self, QtCore.QRect(10, 100, 200, 20), 'Tank Info.', 13 , color[id])
        self.tank_HP = StatLabel(self, QtCore.QRect(10, 125, 200, 20), 'HP: {}'.format(100), 13 , color[id])
        self.tank_ATK = StatLabel(self, QtCore.QRect(10, 150, 200, 20), 'ATK: {}'.format(5), 13 , color[id])
        self.tank_DEF = StatLabel(self, QtCore.QRect(10, 175, 200, 20), 'DEF: {}'.format(2), 13 , color[id])
        self.Home_header = StatLabel(self, QtCore.QRect(10, 200, 200, 20), 'Home Info.', 13 , color[id])
        self.Home_HP = StatLabel(self, QtCore.QRect(10, 225, 200, 20), 'HP: {}'.format(50), 13 , color[id])
        self.Home_DEF = StatLabel(self, QtCore.QRect(10, 250, 200, 20), 'DEF: {}'.format(2), 13 , color[id])

class StatUI(QtWidgets.QFrame):
    def __init__(self, Form, game_info):
        super().__init__(Form)
        self.gmae_info = game_info
        self.setGeometry(QtCore.QRect(self.gmae_info.game_ui_width, 0, self.gmae_info.stat_ui_width, self.gmae_info.stat_ui_height))
        self.setStyleSheet("background-color:#808080") 
        self.setObjectName("stat")

        self.player0 = PlayerInfo(self, QtCore.QRect(0, 0, self.gmae_info.stat_ui_width, self.gmae_info.stat_ui_height/2), 0)
        self.player1 = PlayerInfo(self, QtCore.QRect(0, self.gmae_info.stat_ui_height/2, self.gmae_info.stat_ui_width, self.gmae_info.stat_ui_height/2), 1)
        self.players={0:self.player0, 1:self.player1}

    def update_name(self, id, name):
        self.players[id].name.setText('Name: {}'.format(name))