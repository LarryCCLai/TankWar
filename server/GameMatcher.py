import threading
from GameSocket import GameSocket

class GameMatcher():
    def __init__(self):
        self.wait_list=[]
        self.can_match = False
        self.lock = threading.Lock()
        self.call_count = 0
        self.playing_dict = dict()
        self.port = 20002

    def push(self, player):
        self.lock.acquire()

        self.wait_list.append(player)
        player.priority = len(self.wait_list) - 1
        
        self.lock.release()

    def get_priority(self, name):
        priority = -1
        self.lock.acquire()
        for player in self.wait_list:
            if(player.params['name'] == name):
                priority = player.priority
                break
        self.lock.release()
        return priority
    
    def get_wait_num(self):
        self.lock.acquire()
        length = len(self.wait_list)
        self.lock.release()
        return length

    def update(self):
        del self.wait_list[0]
        del self.wait_list[0]
        self.call_count = 0

    def cancel_match(self, name):
        ret = False
        self.lock.acquire()
        for i in range(len(self.wait_list)):
            if(self.wait_list[i].params['name'] == name):
                del self.wait_list[i]
                ret = True
                break
        self.lock.release()    
        return ret

    def match(self, priority):
        self.lock.acquire()
        self.call_count += 1
        player = None
        
        if(priority == 0):
            player = self.wait_list[1]
            self.port = self.find_port()
        else:
            self.port = self.find_port()
            player = self.wait_list[0]

        player.params['port'] = self.port 

        if(self.call_count == 2):
            self.open_game_socket()
            self.update()

        self.lock.release()
        return player

    def find_port(self):
        self.port = 20002
        while(self.port in self.playing_dict):
            self.port += 1
        return self.port
    
    def open_game_socket(self):
        host = '127.0.0.1'
        game_socket = GameSocket(host, self.port, 2)
        game_socket.setDaemon(True)
        game_socket.serve()
        self.playing_dict[self.port] = {'players':(self.wait_list[0], self.wait_list[1]), 'socket': game_socket}
        
    
    def close_game_socket(self, port):
        self.playing_dict[port]['socket'].terminate()
        self.playing_dict[port]['socket'].server_socket.close()
        del self.playing_dict[port]