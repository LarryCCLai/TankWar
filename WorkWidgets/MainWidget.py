from PyQt5 import QtWidgets, QtGui, QtCore
from WorkWidgets.SignUpWidget import SignUpWidget
from WorkWidgets.SignInWidget import SignInWidget
from WorkWidgets.PlayerWidget import PlayerWidget
from WorkWidgets.GameWidget import GameWidget
from WorkWidgets.HelpWidget import HelpWidget
from WorkWidgets.MenuWidget import MenuWidget
from WorkWidgetComponents import LabelComponent
from WorkWidgetComponents import ButtonComponent
import socket
from requests import get

class MainWidget(QtWidgets.QWidget):
    def __init__(self, client):
        super().__init__()
        
        self.setObjectName("main_widget")

        layout = QtWidgets.QVBoxLayout()

        header_label = LabelComponent(24, "Tank War Online")
        ip_label = LabelComponent(14, 'Your local IP address is: {:14}\nYour public IP address is: {:14}'.format(socket.gethostbyname(socket.gethostname()), get('https://api.ipify.org').text))
        ip_label.setAlignment(QtCore.Qt.AlignRight)
        header_label.setAlignment(QtCore.Qt.AlignCenter)
        function_widget = FunctionWidget(client)
        
        layout.addWidget(header_label, stretch=1)
        layout.addWidget(ip_label, stretch=1)
        layout.addWidget(function_widget, stretch=10)

        # layout.setRowStretch(0, 1)
        # layout.setRowStretch(1, 9)
        # layout.setColumnStretch(0, 2)
        # layout.setColumnStretch(1, 8)
        self.setLayout(layout)
    
    def update_widget(self):
        layout = QtWidgets.QGridLayout()
        self.setLayout(layout)

class FunctionWidget(QtWidgets.QStackedWidget):
    def __init__(self, client):
        self.client = client
        self.game_widget = None
        super().__init__()
        self.widget_dict = {
            "menu": self.addWidget(MenuWidget(self.update_widget)),
            "help": self.addWidget(HelpWidget(self.update_widget)),
            "sign_up": self.addWidget(SignUpWidget(self.client, self.update_widget)),
            "sign_in": self.addWidget(SignInWidget(self.client, self.update_widget)),
            "player": self.addWidget(PlayerWidget(self.client, self.update_widget)),
            "game": -1
        }
        self.update_widget("menu")
    
    def update_widget(self, name, player_info=None, rival_info=None, priority=None):
        if(name == 'game'):
            self.game_widget = GameWidget(self.client, self.update_widget, player_info, rival_info, priority)
            self.widget_dict['game'] = self.addWidget(self.game_widget)
        
        self.setCurrentIndex(self.widget_dict[name])
        current_widget = self.currentWidget()

        if(name =='player'):
            if(self.widget_dict['game'] != -1):
                self.removeWidget(self.game_widget)
                del self.game_widget
                self.game_widget = None
                self.widget_dict['game'] = -1
            current_widget.init(player_info)
        else:
            current_widget.init()

        current_widget.load()
        
        # print('\n====================\nStackWidget Count: {}\n===================\n'.format(self.count()))

        