from PyQt5 import QtWidgets, QtGui, QtCore
from WorkWidgetComponents import LabelComponent, LineEditComponent, ButtonComponent
import json
from WorkWidgets.ExecuteCommand import ExecuteCommand

import json

class SignInWidget(QtWidgets.QWidget):
    def __init__(self, client, update_widget_callback):
        super().__init__()
        layout = QtWidgets.QGridLayout()

        self.client = client
        self.update_widget_callback = update_widget_callback
        self.setObjectName('sign_in_widget')

        header_label = LabelComponent(20, 'Sign In')

        self.back_btn = ButtonComponent('Back')
        self.back_btn.clicked.connect(lambda: self.update_widget_callback("menu"))

        name_label = LabelComponent(16, 'Name ')
        self.name_editor = LineEditComponent('')
        self.name_editor.mousePressEvent = self.clear_name_editor_content
        
        password_label = LabelComponent(16, 'Password ')
        self.password_editor = LineEditComponent('')
        self.password_editor.mousePressEvent = self.clear_password_editor_content
        self.password_editor.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_editor.setMaxLength(16)
        
        self.signin_btn = ButtonComponent('Sign In')
        self.signin_btn.clicked.connect(self.signin_action)
        self.info_label = LabelComponent(16, '')
        
        layout.addWidget(header_label, 0, 0, 1, 2)

        layout.addWidget(self.back_btn, 1, 0, 1, 1)

        layout.addWidget(name_label, 2, 0, 1, 1)
        layout.addWidget(self.name_editor, 2, 1, 1, 1)

        layout.addWidget(password_label, 3, 0, 1, 1)
        layout.addWidget(self.password_editor, 3, 1, 1, 1)

        layout.addWidget(self.signin_btn, 4, 1, 1, 1)
        layout.addWidget(self.info_label, 4, 2, 1, 2)

        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 6)
        layout.setColumnStretch(2, 3)
        layout.setRowStretch(0, 1)
        layout.setRowStretch(1, 1)
        layout.setRowStretch(2, 1)
        layout.setRowStretch(3, 1)
        layout.setRowStretch(4, 1)
        layout.setRowStretch(5, 6)
        self.setLayout(layout)

        self.init()
    
    def load(self):
        print("sign in widget")

    def init(self):
        self.name_editor.setText('')
        self.password_editor.setText('')
        self.name_editor.setText('T1') #test
        self.password_editor.setText('12345') #test
        self.set_info('')

    def set_info(self, info, color='black'):
        self.info_label.setText(info)
        self.info_label.setStyleSheet('color: {}'.format(color))
                
    def clear_name_editor_content(self, event):
        self.name_editor.clear()
        self.info_label.clear()

    def clear_password_editor_content(self, event):
        self.password_editor.clear()

    def proces_signin_result(self, result):
        response = json.loads(result)
        if response['status'] == 'OK':
            self.set_info(info='Sign In Success', color='green')
            self.init()
            self.update_widget_callback('player', response['player_info'])
        else: 
            self.set_info(info=response['reason'], color='red')

    def signin_action(self):
        name = self.name_editor.text()
        password = self.password_editor.text()
        
        if(name != '' and len(password) >= 5):
            self.send_command = ExecuteCommand(self.client, 'sign_in', {'name': name, 'password': password})
            self.send_command.start()
            self.send_command.return_sig.connect(self.proces_signin_result)
        elif(name == ''):
            self.set_info(info='Name Error', color='red')
        else:
            self.set_info(info='Password Error', color='red')


  