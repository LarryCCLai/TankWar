class Play:
    '''
    params:
        name,
        address,
    '''
    def __init__(self, PlayerInfoTable, params):
        self.PlayerInfoTable = PlayerInfoTable
        self.params = params
        self.priority = None
        self.game_matcher = self.params['game_matcher']
        del self.params['game_matcher']

    def execute(self):
        response = None
        self.game_matcher.push(self)
        
        while (True):
            wait_num = self.game_matcher.get_wait_num()
            self.priority = self.game_matcher.get_priority(self.params['name'])
            if(self.priority == -1):
                response = {'status': 'Cancel', 'reason': 'you cancel the matching'}
                break
            if(wait_num >= 2 and (self.priority == 0 or self.priority == 1)):
                rival = self.game_matcher.match(self.priority)
                response = {'status': 'OK', 'priority':self.priority, 'rival_info': rival.params}
                break
            
        return response
        


    