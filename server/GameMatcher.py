import threading
class GameMatcher():
    def __init__(self):
        self.wait_list=[]
        self.can_match = False
        self.lock = threading.Lock()
        self.call_count = 0
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
        if(priority==0):
            player = self.wait_list[1]
        else:
            player = self.wait_list[0]
        if(self.call_count == 2):
            self.update()
        self.lock.release()
        return player

    