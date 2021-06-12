from PyQt5 import QtWidgets, QtGui, QtCore
from WorkWidgetComponents import LabelComponent, LineEditComponent, ButtonComponent
import json
from WorkWidgets.ExecuteCommand import ExecuteCommand

import json

class SignUpWidget(QtWidgets.QWidget):
    def __init__(self, client, update_widget_callback):
        super().__init__()
        layout = QtWidgets.QGridLayout()

        self.client = client
        self.update_widget_callback = update_widget_callback
        self.setObjectName('sign_up_widget')

        header_label = LabelComponent(20, 'Sign Up')

        self.back_btn = ButtonComponent('Back')
        self.back_btn.clicked.connect(lambda: self.update_widget_callback("menu"))

        name_label = LabelComponent(16, 'Name ')
        self.name_editor = LineEditComponent('')
        self.name_editor.mousePressEvent = self.clear_name_editor_content
        self.check_btn = ButtonComponent('Check')
        self.check_btn.clicked.connect(self.check_action)
        self.info0_label = LabelComponent(16, '')
        
        password_label = LabelComponent(16, 'Password ')
        self.password_editor = LineEditComponent('')
        self.password_editor.mousePressEvent = self.clear_password_editor_content
        self.password_editor.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_editor.setMaxLength(16)
        
        self.signup_btn = ButtonComponent('Sign Up')
        self.signup_btn.clicked.connect(self.signup_action)
        self.info1_label = LabelComponent(16, '')
        
        self.info_sel = {0: self.info0_label, 1: self.info1_label}

        layout.addWidget(header_label, 0, 0, 1, 2)

        layout.addWidget(self.back_btn, 1, 0, 1, 1)

        layout.addWidget(name_label, 2, 0, 1, 1)
        layout.addWidget(self.name_editor, 2, 1, 1, 1)
        layout.addWidget(self.check_btn, 2, 2, 1, 1)
        layout.addWidget(self.info0_label, 2, 3, 1, 1)

        layout.addWidget(password_label, 3, 0, 1, 1)
        layout.addWidget(self.password_editor, 3, 1, 1, 1)

        layout.addWidget(self.signup_btn, 4, 1, 1, 1)
        layout.addWidget(self.info1_label, 4, 2, 1, 2)

        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 6)
        layout.setColumnStretch(2, 1)
        layout.setColumnStretch(3, 2)
        
        layout.setRowStretch(0, 1)
        layout.setRowStretch(1, 1)
        layout.setRowStretch(2, 1)
        layout.setRowStretch(3, 1)
        layout.setRowStretch(4, 1)
        layout.setRowStretch(5, 6)
        self.setLayout(layout)

        self.init()
    
    def load(self):
        print("sign up widget")

    def init(self):
        self.student = {'name':'', 'scores':dict()}
        self.name_editor.setText('')
        self.password_editor.setText('')
        self.signup_btn.setEnabled(False)

    def set_info(self, sel, info, color='black'):
        self.info_sel[sel].setText(info)
        self.info_sel[sel].setStyleSheet('color: {}'.format(color))
                
    def clear_name_editor_content(self, event):
        self.signup_btn.setEnabled(False)
        self.info0_label.clear()
        self.info1_label.clear()

    def clear_password_editor_content(self, event):
        self.password_editor.clear()

    def process_check_result(self, result):
        response = json.loads(result)

        if response['status'] == 'Fail':
            self.student['name'] = self.name_editor.text()
            self.set_info(sel=0, info='\'{}\' OK'.format(self.name_editor.text()), color='green')
            self.signup_btn.setEnabled(True)
        elif response['status'] == 'OK':
            self.set_info(sel=0, info='\'{}\' exists\''.format(self.name_editor.text()), color='red')

    def check_action(self):
        if(self.name_editor.text() != ''):
            self.send_command = ExecuteCommand(self.client, 'query', {'name': self.name_editor.text()})
            self.send_command.start()
            self.send_command.return_sig.connect(self.process_check_result)
        else:
            self.set_info(sel=0, info='enter a name', color='red')
    
    def proces_signup_result(self, result):
        response = json.loads(result)
        if response['status'] == 'OK':
            self.set_info(sel=1, info='Sign Up Success'.format(self.student), color='green')
            self.init()
            self.update_widget_callback('menu')

    def signup_action(self):
        password = self.password_editor.text()
        if(len(password) >= 5):
            self.send_command = ExecuteCommand(self.client, 'sign_up', {'name': self.name_editor.text(), 'password': password})
            self.send_command.start()
            self.send_command.return_sig.connect(self.proces_signup_result)
        else:
            self.set_info(sel=1, info='password length must exceed 5', color='red')


  