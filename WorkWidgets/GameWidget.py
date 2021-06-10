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
        self.receive.return_sig.connect(self.synchronize)
        self.setFocus() 

    def show_ui(self):
        self.resize(1080, 672)
        self.game_ui = GameUI(self)
        
    def keyPressEvent(self, e):
        if e.key()==QtCore.Qt.Key_Right:
            self.send_command = GameSend(self.game_client, 'move', {'priority': self.priority, 'direction':'right'})
            self.send_command.start()
            self.game_ui.tank[self.priority].move('right')
        elif e.key()==QtCore.Qt.Key_Up:
            self.send_command = GameSend(self.game_client, 'move', {'priority': self.priority, 'direction':'up'})
            self.send_command.start()
            self.game_ui.tank[self.priority].move('up')
        elif e.key()==QtCore.Qt.Key_Down:
            self.send_command = GameSend(self.game_client, 'move', {'priority': self.priority, 'direction':'down'})
            self.send_command.start()
            self.game_ui.tank[self.priority].move('down')
        elif e.key()==QtCore.Qt.Key_Left:
            self.send_command = GameSend(self.game_client, 'move', {'priority': self.priority, 'direction':'left'})
            self.send_command.start()
            self.game_ui.tank[self.priority].move('left')
        elif e.key()==QtCore.Qt.Key_Space:
            self.send_command = GameSend(self.game_client, 'shoot', {'priority': self.priority})
            self.send_command.start()
            self.game_ui.tank[self.priority].shoot()

    def synchronize(self, result):
        response = json.loads(result)
        print(response)
        command = response['command']
        priority = response['parameters']['priority']
        if (command == 'move'):
            direction = response['parameters']['direction']
            self.game_ui.tank[priority].move(direction)
        elif(command == 'shoot'):
            self.game_ui.tank[priority].shoot()


    