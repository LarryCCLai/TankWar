from PyQt5 import QtWidgets, QtGui, QtCore
from WorkWidgetComponents import LabelComponent, LineEditComponent, ButtonComponent
import json
from WorkWidgets.ExecuteCommand import ExecuteCommand
from WorkWidgets.RepeatingTimer import RepeatingTimer
import threading
from threading import Timer
import json
from client.SocketClient import SocketClient

host = "127.0.0.1"
port = 20001
cancel_lock = threading.Lock()
cancel_client = SocketClient(host, port)

class PlayerWidget(QtWidgets.QWidget):
    def __init__(self, client, update_widget_callback):
        super().__init__()
        layout = QtWidgets.QGridLayout()
        self.game_client = None
        self.game_server = None
        self.client = client
        self.update_widget_callback = update_widget_callback
        self.player_info = None
        self.timer = None
        self.wait_time = 0
        self.setObjectName('player_widget')

        header_label = LabelComponent(20, 'Player Information')

        self.name_label = LabelComponent(16, 'Name: ')
        self.win_label = LabelComponent(16, 'Win: ')
        self.loss_label = LabelComponent(16, 'Loss: ')
        self.win_ratio_label = LabelComponent(16, 'Win(%): ')
        
        self.sign_out_btn = ButtonComponent('Sign Out')
        self.sign_out_btn.clicked.connect(self.sign_out_action)

        self.play_btn = ButtonComponent('Play')
        self.play_btn.clicked.connect(self.play_action)
        
        self.info_label = LabelComponent(16, '')
        # self.leaderboard_btn = ButtonComponent('Leaderboard')
        
        layout.addWidget(header_label, 0, 0, 1, 2)
        layout.addWidget(self.name_label, 1, 0, 1, 1)
        layout.addWidget(self.win_label, 2, 0, 1, 1)
        layout.addWidget(self.loss_label, 3, 0, 1, 1)
        layout.addWidget(self.win_ratio_label, 4, 0, 1, 1)
        layout.addWidget(self.sign_out_btn, 6, 0, 1, 1)
        layout.addWidget(self.play_btn, 7, 0, 1, 1)
        layout.addWidget(self.info_label, 8, 0, 1, 1)

        layout.setRowStretch(0, 1)
        layout.setRowStretch(1, 1)
        layout.setRowStretch(2, 1)
        layout.setRowStretch(3, 1)
        layout.setRowStretch(4, 1)
        layout.setRowStretch(5, 1)
        layout.setRowStretch(6, 1)
        layout.setRowStretch(7, 1)
        layout.setRowStretch(8, 5)
        self.setLayout(layout)

    def load(self):
        print("player widget")

    def init(self, player_info=None):
        self.player_info = player_info
        self.name_label.setText('Name: {}'.format(player_info['name']))
        self.win_label.setText('Win: {}'.format(player_info['win']))
        self.loss_label.setText('Loss: {}'.format(player_info['loss']))
        
        total = float(player_info['win']) + float(player_info['loss'])
        try:
            win_ratio = float(player_info['win']) / total * 100
        except:
            self.win_ratio_label.setText('Win(%): --')
        else:
            win_ratio = round(win_ratio, 2)
            self.win_ratio_label.setText('Win(%): {}'.format(win_ratio))

    def set_info(self, info, color='black'):
        self.info_label.setText(info)
        self.info_label.setStyleSheet('color: {}'.format(color))

    def update_waiting_match_time(self):
        self.wait_time += 1
        self.set_info('Wait time: {}'.format(self.wait_time))
    
    def sign_out_action(self):
        self.update_widget_callback('menu')
    
    def proces_play_result(self, result):
        '''
        response OK :
            priority,
            rival_info,
        '''
        response = json.loads(result)
        if response['status'] == 'OK':
            self.timer.stop()
            priority = response['priority']
            rival_info = response['rival_info']
            rival_name = rival_info['name']
            rival_address = rival_info['address']
            self.set_info(info='Match Success\n priority = {}\n rival = {}, {}'.format(priority, rival_name, rival_address), color='green')
            self.play_btn.setText('Play')
            self.update_widget_callback('game', self.player_info, rival_info, priority)

            
        
    def proces_cancel_result(self, result):
        response = json.loads(result)
        if response['status'] == 'OK':
            self.timer.stop()
            self.play_btn.setText('Play')
            self.set_info('Cancel Matching Success',color='green')

    def play_action(self):
        if(self.play_btn.text()=='Play'):
            name = self.player_info['name']
            self.send_command = ExecuteCommand(self.client, 'play', {'name': name})
            self.send_command.start()
            self.send_command.return_sig.connect(self.proces_play_result)
            self.play_btn.setText('Cancel')
            self.wait_time = 0
            self.timer = RepeatingTimer(1.0, self.update_waiting_match_time)
            self.timer.start()
        else:

            name = self.player_info['name']
            cancel_lock.acquire()
            self.send_command = ExecuteCommand(cancel_client, 'cancel', {'name': name})
            self.send_command.start()
            self.send_command.return_sig.connect(self.proces_cancel_result)
            cancel_lock.release()

  