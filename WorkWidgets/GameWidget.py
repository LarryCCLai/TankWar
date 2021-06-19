from WorkWidgets.ExecuteCommand import ExecuteCommand
from PyQt5 import QtWidgets, QtGui, QtCore
from WorkWidgetComponents import LabelComponent, LineEditComponent, ButtonComponent
from WorkWidgets.GameSend import GameSend
from WorkWidgets.GameReceive import GameReceive 
import json
from client.SocketClient import SocketClient
from TankWarGame.GameInfo import GameInfo
from TankWarGame.Background import Background
from TankWarGame.GameUI import GameUI
from TankWarGame.StatUI import StatUI
from  TankWarGame.Map.Map import Map

class GameWidget(QtWidgets.QWidget):
    def __init__(self, client, update_widget_callback, player0_info, player1_info, priority):
        super().__init__()
        
        self.client = client
        self.update_widget_callback = update_widget_callback
        self.player_info = {0: player0_info, 1: player1_info}
        self.priority = priority
        self.game_info = GameInfo()
        self.show_ui()
        print(self.player_info[0])
        print(self.player_info[1])
        self.stat_ui.update_name(0, self.player_info[0]['name'])
        self.stat_ui.update_name(1, self.player_info[1]['name'])
        self.flag = True
    def load(self):
        print("game widget")

    def init(self):
        if(self.priority == 0):
            self.game_client = SocketClient(self.client.host, self.player_info[1]['port'])
        else:
            self.game_client = SocketClient(self.client.host, self.player_info[0]['port'])
        self.receive = GameReceive(self.game_client)
        self.receive.start()
        self.receive.return_sig.connect(self.synchronize)
        self.setFocus()

    def show_ui(self):
        self.resize(self.game_info.ui_width, self.game_info.ui_height)
        self.game_info.map_dict = Map(self.game_info.game_ui_width, self.game_info.game_ui_height, self.game_info.bsize).read_map()
        self.game_ui = GameUI(self, self.game_info)
        self.stat_ui = StatUI(self, self.game_info)
        self.stat_ui.close_button.clicked.connect(self.closeButtonEvent)
        self.game_ui.game_over.stateChanged.connect(self.gameOverEvent)
        
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
        command = response['command']
        priority = response['parameters']['priority']
        if (command == 'move'):
            direction = response['parameters']['direction']
            self.game_ui.tank[priority].move(direction)
        elif(command == 'shoot'):
            self.game_ui.tank[priority].shoot()
        elif(command == 'update'):
            self.game_ui.tank[priority].update()
        elif(command == 'close'):
            self.close_gamesocket_server()
    def gameOverEvent(self):
        self.receive.terminate()
        
        if(self.priority == self.game_info.winner):
            self.game_info.win_music.play()
            self.player_info[self.priority]['win'] += 1
            self.send_command = ExecuteCommand(self.client, 'update', {'name': self.player_info[self.priority]['name'], 'result': 'win'})
        else:
            self.game_info.loss_music.play()
            self.player_info[self.priority]['loss'] += 1
            self.send_command = ExecuteCommand(self.client, 'update', {'name': self.player_info[self.priority]['name'], 'result': 'lose'})
        
        self.send_command.start()
    
    def closeButtonEvent(self):
        self.close_gamesocket_client()

    def close_gamesocket_client(self):
        self.game_client.send_command('close', '0')
        
    def close_gamesocket_server(self):
        if(self.priority == 0):
            self.send_close_gamesocket = ExecuteCommand(self.client, 'close_game_socket', {'port': self.player_info[1]['port']})
            self.send_close_gamesocket.start()
            self.send_close_gamesocket.return_sig.connect(self.return_player)
        else:
            self.return_player()

    def return_player(self):
        if(self.priority == 0):
            self.update_widget_callback('player', self.player_info[0])
        else:
            self.update_widget_callback('player', self.player_info[1])