from PyQt5 import QtWidgets, QtGui, QtCore
from WorkWidgetComponents import LabelComponent
from WorkWidgetComponents import ButtonComponent

class MenuWidget(QtWidgets.QWidget):
    def __init__(self, update_widget_callback):
        super().__init__()
        self.setObjectName("menu_widget")
        self.update_widget_callback = update_widget_callback

        layout = QtWidgets.QGridLayout()
        menu_label = LabelComponent(18, "Menu")
        sign_up_button = ButtonComponent("Sign Up")
        sign_in_button = ButtonComponent("Sign In")        
        help_button = ButtonComponent("Help")

        sign_up_button.clicked.connect(lambda: self.update_widget_callback("sign_up"))
        sign_in_button.clicked.connect(lambda: self.update_widget_callback("sign_in"))
        help_button.clicked.connect(lambda: self.update_widget_callback("help"))
        layout.addWidget(menu_label, 0, 0, 1, 1)
        layout.addWidget(sign_up_button, 1, 0, 1, 1)
        layout.addWidget(sign_in_button, 2, 0, 1, 1)
        layout.addWidget(help_button, 3, 0, 1, 1)
        layout.setRowStretch(0, 1)
        layout.setRowStretch(1, 1)
        layout.setRowStretch(2, 1)
        layout.setRowStretch(3, 1)
        layout.setRowStretch(4, 6)
        self.setLayout(layout)
    def load(self):
        print("menu widget")

    def init(self):
        None