from PyQt5 import QtWidgets, QtGui, QtCore
from WorkWidgetComponents import LabelComponent, LineEditComponent, ButtonComponent
from WorkWidgets.ExecuteCommand import ExecuteCommand
import json

from TankWarGame.GameUI import GameUI

class GameWidget(QtWidgets.QWidget):
    def __init__(self, client, update_widget_callback):
        super().__init__()
        layout = QtWidgets.QGridLayout()

        self.client = client
        self.update_widget_callback = update_widget_callback
        self.player_info = None
        self.rival_info = None
        self.priority = None
        self.setObjectName('sign_up_widget')

        header_label = LabelComponent(20, 'GameWidget')
        
        layout.addWidget(header_label, 0, 0, 1, 2)

        layout.setColumnStretch(0, 1)
        
        layout.setRowStretch(0, 1)
        self.setLayout(layout)

        self.init()
    
    def load(self):
        print("game widget")

    def init(self, player_info=None, rival_info=None, priority=None):
        self.player_info = player_info
        self.rival_info = rival_info
        self.priority = priority
        self.show_ui()

    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def show_fuui(self, Form):
        self.stat_ui = QtWidgets.QFrame(Form)
        self.stat_ui.setGeometry(QtCore.QRect(840, 0, 240, 672))
        self.stat_ui.setStyleSheet("background-color:#808080") 
        self.stat_ui.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.stat_ui.setFrameShadow(QtWidgets.QFrame.Raised)
        self.stat_ui.setObjectName("stat")
        
    def show_ui(self):
        self.resize(1080, 672)
        self.game_ui = GameUI(self)

        self.setFocus() # 把self界面设置为焦点，以响应键盘事件
        self.show_fuui(self)
            