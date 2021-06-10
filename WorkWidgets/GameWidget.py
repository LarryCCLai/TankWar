from PyQt5 import QtWidgets, QtGui, QtCore
from WorkWidgetComponents import LabelComponent, LineEditComponent, ButtonComponent
from WorkWidgets.GameSend import GameSend
from WorkWidgets.GameReceive import GameReceive 
import json
from client.SocketClient import SocketClient
from TankWarGame.GameUI import GameUI
from TankWarGame.StatUI import StatUI
from TankWarGame.Tank.Tank import Tank

class GameWidget(QtWidgets.QWidget):
    def __init__(self, client, update_widget_callback):
        super().__init__()
        self.game_client = None
        self.client = client
        self.update_widget_callback = update_widget_callback
        self.player_info = {0: None, 1: None}
        self.priority = None
        self.receive = None
        self.show_ui()
        self.setObjectName('sign_up_widget')

        # self.init()
    
    def load(self):
        print("game widget")

    def init(self, player0_info=None, player1_info=None, priority=None):
        self.player_info[0] = player0_info
        self.player_info[1] = player1_info
        self.priority = priority
        print(self.player_info[0])
        print(self.player_info[1])
        if(self.priority == 0):
            self.game_client = SocketClient(self.client.host, self.player_info[1]['port'])
        else:
            self.game_client = SocketClient(self.client.host, self.player_info[0]['port'])

        self.receive = GameReceive(self.game_client)
        self.receive.start()
        self.receive.return_sig.connect(self.check)
        self.setFocus() 

    def show_ui(self):
        self.resize(1080, 672)
        self.game_ui = GameUI(self)
        
    # def RecvCommand

    def keyPressEvent(self, e):
        if e.key()==QtCore.Qt.Key_Right:
            self.send_command = GameSend(self.game_client, 'right', {'priority': self.priority})
            self.send_command.start()
            # self.game_ui.tank[self.priority].move('right')
        # elif e.key()==QtCore.Qt.Key_Up:
            # self.game_ui.tank[self.priority].move('up')
        # elif e.key()==QtCore.Qt.Key_Down:
            # self.game_ui.tank[self.priority].move('down')
        # elif e.key()==QtCore.Qt.Key_Left:
            # self.game_ui.tank[self.priority].move('left')
        # elif e.key()==QtCore.Qt.Key_Space:
            # self.game_ui.tank[self.priority].shoot()

    def check(self, result):
        response = json.loads(result)
        print(response)
    # def center(self):
    #     qr = self.frameGeometry()
    #     cp = QtWidgets.QDesktopWidget().availableGeometry().center()
    #     qr.moveCenter(cp)
    #     self.move(qr.topLeft())

    