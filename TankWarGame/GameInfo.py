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

        self.ui_width = 1080
        self.ui_height = 672
        self.game_ui_width = 864
        self.game_ui_height = 672
        self.stat_ui_width = 240
        self.stat_ui_height = 672
        self.bsize = 24

        #used to initilize 
        self.tank_hp = 100
        self.tank_atk = 10
        self.tank_speed = 1       # map unit
        self.home_hp = 100
        self.bullet_speed = 12     #pixel

        self.re_time = 2           #s

        self.self_id = None
        self.rival_id = None

        self.map_dict = None

        self.static_objs = dict()  #key: coord
        self.tank_objs = None    #key: coord
        self.home_objs = None
        self.bullet_life = {0:False, 1:False}
        
        self.food_obj = None  
        
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