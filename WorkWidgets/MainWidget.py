from PyQt5 import QtWidgets, QtGui, QtCore
from WorkWidgets.SignUpWidget import SignUpWidget
from WorkWidgets.SignInWidget import SignInWidget
from WorkWidgets.PlayerWidget import PlayerWidget
from WorkWidgets.GameWidget import GameWidget
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

class MenuWidget(QtWidgets.QWidget):
    def __init__(self, update_widget_callback):
        super().__init__()
        self.setObjectName("menu_widget")
        self.update_widget_callback = update_widget_callback

        layout = QtWidgets.QGridLayout()
        menu_label = LabelComponent(18, "Menu")
        sign_up_button = ButtonComponent("Sign Up")
        sign_in_button = ButtonComponent("Sign In")        

        sign_up_button.clicked.connect(lambda: self.update_widget_callback("sign_up"))
        sign_in_button.clicked.connect(lambda: self.update_widget_callback("sign_in"))
        layout.addWidget(menu_label, 0, 0, 1, 1)
        layout.addWidget(sign_up_button, 1, 0, 1, 1)
        layout.addWidget(sign_in_button, 2, 0, 1, 1)
        layout.setRowStretch(0, 1)
        layout.setRowStretch(1, 1)
        layout.setRowStretch(2, 1)
        layout.setRowStretch(3, 7)
        self.setLayout(layout)
    def load(self):
        print("menu widget")

    def init(self):
        None

class FunctionWidget(QtWidgets.QStackedWidget):
    def __init__(self, client):
        self.client = client
        super().__init__()
        self.widget_dict = {
            "menu": self.addWidget(MenuWidget(self.update_widget)),
            "sign_up": self.addWidget(SignUpWidget(self.client, self.update_widget)),
            "sign_in": self.addWidget(SignInWidget(self.client, self.update_widget)),
            "player": self.addWidget(PlayerWidget(self.client, self.update_widget)),
            "game": self.addWidget(GameWidget(self.client, self.update_widget))
        }
        self.update_widget("menu")
    
    def update_widget(self, name, player_info=None, rival_info=None, priority=None):
        self.setCurrentIndex(self.widget_dict[name])
        current_widget = self.currentWidget()
        if(name =='player'):
            current_widget.init(player_info)
        elif(name == 'game'):
            current_widget.init(player_info, rival_info, priority)
        else:
            current_widget.init()
        current_widget.load()

        