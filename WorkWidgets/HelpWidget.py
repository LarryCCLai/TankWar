from PyQt5 import QtWidgets, QtCore
from WorkWidgetComponents import LabelComponent
from WorkWidgetComponents import ButtonComponent

class HelpWidget(QtWidgets.QWidget):
    def __init__(self, update_widget_callback):
        super().__init__()
        self.setObjectName("help_widget")
        self.update_widget_callback = update_widget_callback

        layout = QtWidgets.QGridLayout()
        header_label = LabelComponent(18, "Help")

        help_control = ControlTankHelpWidget()
        help_bonus = BounsHelpWidget()
        help_bullet_level = BulletLevelHelpWidget()

        back_btn = ButtonComponent('Back')
        back_btn.clicked.connect(lambda: self.update_widget_callback("menu"))

        layout.addWidget(header_label, 0, 0, 1, 1)
        layout.addWidget(help_control, 1, 0, 1, 1)
        layout.addWidget(help_bonus, 2, 0, 1, 2)        
        layout.addWidget(help_bullet_level, 3, 0, 1, 2)
        layout.addWidget(back_btn, 4, 0, 1, 2)

        layout.setRowStretch(0, 1)
        layout.setRowStretch(1, 1)
        layout.setRowStretch(2, 1)
        layout.setRowStretch(3, 1)
        layout.setRowStretch(4, 1)
        layout.setRowStretch(5, 7)
        # layout.setColumnStretch(0,)
        self.setLayout(layout)

    def load(self):
        print("help widget")

    def init(self):
        None

class ControlTankHelpWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QGridLayout()
        header_label = LabelComponent(16, "1.Control Tank")
        shoot_label = LabelComponent(16, "Shoot")
        shoot_label.setAlignment(QtCore.Qt.AlignCenter)
        move_label = LabelComponent(16, "Move")
        move_label.setAlignment(QtCore.Qt.AlignCenter)
        move_image = QtWidgets.QPushButton()
        move_image.setText('')
        move_image.setStyleSheet('QPushButton{border-image:url(./TankWarGame/Image/help/move.png);}')
        move_image.setFixedSize(QtCore.QSize(226,150))
        move_image.setEnabled(True)

        shoot_image = QtWidgets.QPushButton()
        shoot_image.setText('')
        shoot_image.setStyleSheet('QPushButton{border-image:url(./TankWarGame/Image/help/shoot.png);}')
        shoot_image.setFixedSize(QtCore.QSize(226,150))
        shoot_image.setEnabled(True)
        layout.addWidget(header_label, 0, 0, 1, 2)
        layout.addWidget(shoot_image, 1, 1, 1, 1)
        layout.addWidget(move_image, 1, 2, 1, 1)

        layout.addWidget(shoot_label, 2, 1, 1, 1)
        layout.addWidget(move_label, 2, 2, 1, 1)

        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 5)
        layout.setColumnStretch(2, 4)
        layout.setColumnStretch(3, 2)
        self.setLayout(layout)

class BounsHelpWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QGridLayout()

        header_label = LabelComponent(16, "2. Bouns")
        bullet_lavelup_image = QtWidgets.QPushButton()
        bullet_lavelup_image.setText('')
        bullet_lavelup_image.setStyleSheet('QPushButton{border-image:url(./TankWarGame/Image/bonus/star.png);}')
        bullet_lavelup_image.setFixedSize(QtCore.QSize(48,48))
        bullet_lavelup_image.setEnabled(False)
        bullet_lavelup_label = LabelComponent(16, ": Upgrade Bullet level")
        bullet_lavelup_label.setAlignment(QtCore.Qt.AlignVertical_Mask)
        layout.addWidget(header_label, 0, 0, 1, 2)
        layout.addWidget(bullet_lavelup_image, 1, 1, 1, 1)
        layout.addWidget(bullet_lavelup_label, 1, 2, 1, 1)

        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 2)
        layout.setColumnStretch(2, 5)
        # layout.setColumnStretch(3, 4)
        self.setLayout(layout)

class BulletLevelHelpWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QGridLayout()

        header_label = LabelComponent(16, "3. Bullet Level")
        
        level_1_label = LabelComponent(16, "Level 1: bullet can break brick wall")
        level_2_label = LabelComponent(16, "Level 2: bullet can break iron wall")
        
        brick_wall_image = QtWidgets.QPushButton()
        brick_wall_image.setText('')
        brick_wall_image.setStyleSheet('QPushButton{border-image:url(./TankWarGame/Image/scene/brick.png);}')
        brick_wall_image.setFixedSize(QtCore.QSize(48,48))
        brick_wall_image.setEnabled(False)

        iron_wall_image = QtWidgets.QPushButton()
        iron_wall_image.setText('')
        iron_wall_image.setStyleSheet('QPushButton{border-image:url(./TankWarGame/Image/scene/iron.png);}')
        iron_wall_image.setFixedSize(QtCore.QSize(48,48))
        iron_wall_image.setEnabled(False)

        bullet_lavelup_label = LabelComponent(16, ": Upgrade Bullet level")
        bullet_lavelup_label.setAlignment(QtCore.Qt.AlignVertical_Mask)

        layout.addWidget(header_label, 0, 0, 1, 2)

        layout.addWidget(level_1_label, 1, 1, 1, 1)
        layout.addWidget(brick_wall_image, 1, 2, 1, 1)

        layout.addWidget(level_2_label, 2, 1, 1, 1)
        layout.addWidget(iron_wall_image, 2, 2, 1, 1)

        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 5)
        layout.setColumnStretch(2, 2)
        layout.setColumnStretch(3, 4)
        self.setLayout(layout)