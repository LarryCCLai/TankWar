import pygame

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

        self.game_ui_width = 864
        self.game_ui_height = 672
        self.stat_ui_width = 240
        self.stat_ui_height = 672
        self.bsize = 24

        self.map_dict = None

        self.static_objs = dict()  #key: dim
        self.tank_dict = dict()    #key: dim

        self.main_obj = None
        self.background = None

        self.bullet_life = {0:False, 1:False}

        self.bullet_type_dict = {}
        self.laoying = None   #  老鹰对象
        
        self.food_obj = None  #  食物对象
        #  我方坦克子弹线程标志位，False表示为线程不在运行
        self.frame_one = None   
        
        pygame.init()
        pygame.mixer.init()
        self.volume = 1
        
        self.bullet_music = pygame.mixer.Sound("./TankWarGame/Audios/bang.wav")
        self.bullet_music.set_volume(self.volume*0.2)
        
        self.start_music = pygame.mixer.Sound("./TankWarGame/Audios/start.wav")
        self.start_music.set_volume(self.volume*0.6)
        
        self.win_music = pygame.mixer.Sound("./TankWarGame/Audios/victory.wav")
        self.win_music.set_volume(self.volume)

        self.loss_music = pygame.mixer.Sound("./TankWarGame/Audios/sb2.wav")
        self.loss_music.set_volume(self.volume)

        self.bouns_music = pygame.mixer.Sound("./TankWarGame/Audios/add.wav")
        self.bouns_music.set_volume(self.volume)