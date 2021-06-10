import csv
import random
map_file = {0:'./TankWarGame/Map/map1.csv',
            1:'./TankWarGame/Map/map2.csv'}

b_size = 24
game_ui_width = 840
game_ui_height = 672

class Map:
    def __init__(self):
        self.map_dict = dict()
        self.w_num = game_ui_width/b_size
        self.h_num = game_ui_height/b_size

    def read_map(self):
        # sel = random.randint(0, 1)
        sel = 1
        y = 0
        with open(map_file[sel],'r',newline='') as f:
            rows = csv.reader(f)
            for row in rows:
                # print(row)
                for x in range(int(self.w_num)):
                    if(row[x]==''):
                        continue
                    self.map_dict[(x,y)] = int(row[x])
                y+=1
                
        return self.map_dict