from GameMatcher import GameMatcher
game_matcher = GameMatcher()

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
        
    def execute(self):
        response = None
        game_matcher.push(self)
        
        while (True):
            wait_num = game_matcher.get_wait_num()
            self.priority = game_matcher.get_priority(self.params['name'])
            if(self.priority == -1):
                response = {'status': 'Cancel', 'reason': 'you cancel the matching'}
                break
            if(wait_num >= 2 and (self.priority == 0 or self.priority == 1)):
                rival = game_matcher.match(self.priority)
                response = {'status': 'OK', 'priority':self.priority, 'rival_info': rival.params}
                break
        return response
        
class Cancel:
    '''
    params:
        name,
    '''
    def __init__(self, PlayerInfoTable, params):
        self.PlayerInfoTable = PlayerInfoTable
        self.params = params
        self.priority = None
        
    def execute(self):
        response = None
        if(game_matcher.cancel_match(self.params['name'])):
            response = {'status': 'OK', 'reason': 'you cancel the matching'}
        else:
            response = {'status': 'Fail', 'reason': 'Cancel Faild'}
            # shouldn't occur
        return response


    