import sys
import threading
import time

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton

# from Bullet import bullet
# from Global import quan_var
# from Worker import work_bullet

class Tank(QtWidgets.QPushButton):
    def __init__(self, game_ui, x, y, id, direction):
        super().__init__(game_ui)
        self.id = id
        self.init_x = x
        self.init_y = y
        self.cur_x = x        
        self.cur_y = y        
        self.direction = direction    
        self.life = 1000
        self.attack = 5
        self.defense = 2
        self.tank_speed = 1
        self.bullet_speed = 1
        self.lock = threading.Lock()

        self.change_direction(direction)
        self.setGeometry(x*game_ui.b_size, y*game_ui.b_size, game_ui.b_size*2, game_ui.b_size*2)
    
    def change_direction(self, direction):
        self.direction = direction
        self.setStyleSheet('QPushButton{border-image:url(./TankWarGame/Image/tank/tank%s_%s.png);}' % (self.id, direction))
            
    # def chusheng(self, frame):# 18*26
    #     self.frame = frame
    #     # 玩家控件
    #     self.tank_player = QPushButton(frame)
    #     #  设置位置大小
    #     self.tank_player.setGeometry(self.x, self.y, 48, 48)
    #     #  self.tank_player.setGeometry(18*24, 26*24, 48, 48)
    #     # 根据是玩家一还是玩家二，显示相应的颜色
    #     self.tank_qiehuan()
    #     # 将坦克位置信息同步到全局变量中
    #     self.gengxin_map_dict(self.x//24, self.y//24)
    #     #  根据像素点 存放我方坦克对象
    #     self.flag_mytank()

    # def update_map_dict(self, x, y):  # 更新map_dict中的我方坦克位置
    #     #  给修改操作加锁，避免高并发出错
    #     self.lock.acquire(timeout=0.02)
    #     x-=1
    #     y-=1
    #     quan_var.map_dict[(x, y)] = self.flag
    #     quan_var.map_dict[(x + 1, y)] = self.flag
    #     quan_var.map_dict[(x, y + 1)] = self.flag
    #     quan_var.map_dict[(x + 1, y + 1)] = self.flag
    #     self.lock.release()

    # # 更新mytank_dict字典中的我方坦克信息
    # def flag_mytank(self):
    #     self.lock.acquire(timeout=0.02)
    #     for key, value in quan_var.mytank_dict.copy().items():
    #         if value==self:
    #             del quan_var.mytank_dict[key]
    #     quan_var.mytank_dict[(self.x, self.y)] = self
    #     self.lock.release()

    # def shoot(self): 
    #     if not quan_var.thread_life:
    #         quan_var.thread_life = True
    #         self.bu = bullet(self.frame, self, self.tank_player)
    #         try:
    #             self.work = work_bullet(self.bu)
    #             self.thread = QThread()
    #             self.work.moveToThread(self.thread)
    #             self.work.fa_bullet_singnal.connect(self.bu.move)
    #             self.work.jieshu1.connect(lambda: self.thread.quit())
    #             self.thread.started.connect(self.work.fa_bullet)
    #             self.thread.start()
    #         except Exception as e:
    #             print(e,'发射子弹错误')

    # def get_life(self):
    #     if quan_var.life_list.get(self, 0):
    #         quan_var.life_list[self].setText('%s'%self.life)

    # def dead(self): 
    #     self.gengxin_map_dict(self.x//24, self.y//24)  # 清除死亡位置足迹
    #     #  生命值大于一，即生命值减一
    #     if self.life>1:
    #         self.life-=1
    #         #  可添加被击中效果
    #         #  对玩家一的操作
    #         if not self.tank_two:
    #             self.tank_player.setGeometry(17*24, 25*24, 48, 48)  # 玩家一回到初始位置
    #             self.x, self.y = 17*24, 25*24
    #         else:
    #             self.tank_player.setGeometry(9 * 24, 25 * 24, 48, 48)  #  玩家二回到初始位置
    #             self.x, self.y = 9 * 24, 25 * 24
            
    #         self.gengxin_map_dict(self.x//24, self.y//24) # 更新出生位置
    #         self.flag_mytank()  #  更新我方坦克 位置对象 字典
    #         self.get_life()
    #     #  生命值为一被击中的时候，清除坦克
    #     else:
    #         del quan_var.mytank_dict[(self.x, self.y)]
    #         self.tank_player.setVisible(False)
    #         self.flag = 0
    #         self.get_life()
    #     #  我方坦克全部死亡，游戏结束，判输
    #     if not quan_var.mytank_dict:
    #         self.gameover = QLabel(quan_var.frame_one)
    #         self.gameover.setGeometry(86, 172, 497, 249)
    #         self.gameover.setStyleSheet('QLabel{border-image:url(./image/home/timg.png)}')
    #         self.gameover.setWindowOpacity(0.4)
    #         self.gameover.setVisible(True)
    #         QApplication.processEvents()
    #         quan_var.defeat.play()
    #         time.sleep(1.2)
    #         print('jie shu you xi')
    #         #  sys.exit(QApplication(sys.argv).exec_())
    #         sys.exit(0)
    # #  坦克移动函数
    # def move(self, direction):
    #     self.change_direction(direction)

    #     qian_flag = self.is_qian()

    #     if max(qian_flag) <= 1:
    #         if max(qian_flag) == 0.1:  #  手雷
    #             quan_var.add_food.play()
    #             quan_var.food_obj.siwang()
    #             mytank_obj_list = list(quan_var.mytank_dict.values())
    #             for enytank in quan_var.life_list:
    #                 if enytank not in mytank_obj_list:
    #                     print('调用敌方坦克siwang')
    #                     enytank.siwang()
    #         elif max(qian_flag) == 0.2:  #  五角星
    #             quan_var.food_obj.siwang()
    #             quan_var.add_food.play()
    #             self.bullet_type += 1
    #             quan_var.bullet_type_dict[self] = self.bullet_type
    #         elif max(qian_flag) == 0.3:  #  生命值
    #             quan_var.add_food.play()
    #             quan_var.food_obj.siwang()
    #             self.life += 1
    #             quan_var.mytank_life = self.life
    #             self.get_life()
    #         else:
    #             pass

    #         self.flag = 0
    #         self.gengxin_map_dict(self.x//24, self.y//24)  #  清除之前map_dict上mytank的位置
    #         #  运动之后的坐标（单位像素）
    #         self.x = self.x+self.fangxiang[0] * quan_var.mytank_speed
    #         self.y += self.fangxiang[1] * quan_var.mytank_speed
    #         if quan_var.food_dict.get((self.x, self.y), 0):
    #             quan_var.food_dict.get((self.x, self.y), 0).siwang()
    #         #  改变其对应位置
    #         self.tank_player.setGeometry(self.x, self.y, 48,48)
    #         #  self.changSudu()
    #         self.flag = 5
    #         self.gengxin_map_dict(self.x//24, self.y//24)  #  更新map_dict   玩家一位置
    #         #  更新quan_var.mytank_dict列表
    #         self.flag_mytank()

    # #  判断坦克能否往前  返回类型（标志数，标志数） 告诉move方法 坦克前面是什么
    # def is_qian(self, direction):
    #     x,y = self.x, self.y
    #     if self.fangxiang=='right':
    #         return quan_var.map_dict.get((x // 24 + 1 , y // 24 - 1), 0), quan_var.map_dict.get((x // 24 + 1  , y // 24 ), 0)
    #     elif self.fangxiang==(-1, 0): #  方向为左
    #         #  左上                                                                                左下
    #         self.change_direction('left')
    #         return quan_var.map_dict.get(((x-quan_var.mytank_speed) // 24 - 1, y // 24 - 1), 0), quan_var.map_dict.get(((x-quan_var.mytank_speed) // 24 - 1, y // 24), 0)
    #     elif self.fangxiang==(0, 1): # 方向为下
    #         #  左下                                                          右下
    #         self.change_direction('down')
    #         return quan_var.map_dict.get((x // 24 - 1, y // 24 + 1), 0), quan_var.map_dict.get((x // 24, y // 24 + 1), 0)
    #     else :  # 方向为上
    #         #  左上                                                                               右上
    #         self.change_direction('up')
    #         return quan_var.map_dict.get((x // 24 - 1, (y - quan_var.mytank_speed) // 24 - 1), 0), quan_var.map_dict.get((x // 24, (y - quan_var.mytank_speed) // 24 - 1), 0)
    
    #  改变坦克速度函数，未被调用
    # def changSudu(self):
    #     for i in range(1, 5):
    #         self.x = self.x + self.fangxiang[0] * quan_var.mytank_speed//4
    #         self.y += self.fangxiang[1] * quan_var.mytank_speed//4
    #         self.tank_player.setGeometry(self.x, self.y, 48, 48)
    #         time.sleep(0.05)
