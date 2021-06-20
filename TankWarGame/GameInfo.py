class GameInfo:
    def __init__(self):
    
        self.tank0 = 0
        self.tank1 = 1
        self.tree = 2
        self.brick_wall = 3
        self.iron_wall = 4
        self.home = 5
        self.border = 6
        self.none = 7
        self.home0 = 8
        self.home1 = 9
        self.game_over = False
        self.loser = None
        self.winner = None

        self.ui_width = 1080
        self.ui_height = 672
        self.game_ui_width = 864
        self.game_ui_height = 672
        self.stat_ui_width = 240
        self.stat_ui_height = 672
        self.bsize = 24

        self.coord_left_x = 0
        self.coord_left_y = 0
        self.coord_right_x = self.game_ui_width//self.bsize
        self.coord_right_y = self.game_ui_height//self.bsize
        
        #used to initilize 
        self.tank_hp = 100
        self.tank_atk = 10
        self.tank_speed = 1       # map unit
        self.home_hp = 100
        self.bullet_speed = 12     #pixel
        self.bullet_level = 1     #1 or 2
        self.rebirth_time = 1           #s
        
        
        self.priority = None    
        
        self.stat_ui = None
        self.map_dict = None

        self.static_objs = dict()  #key: coord
        self.tank_objs = {0:None, 1:None}    
        self.home_objs = {0:None, 1:None}
        self.bonus_obj = None
        
        self.bonus_worker = None
        self.bonus_type = None
        self.bonus_locate = list()
        self.bonus_tank = 0.1
        self.bonus_star = 0.2