class Cancel:
    '''
    params:
        name,
    '''
    def __init__(self, PlayerInfoTable, params):
        self.PlayerInfoTable = PlayerInfoTable
        self.params = params
        self.priority = None
        self.game_matcher = self.params['game_matcher']
        del self.params['game_matcher']
    def execute(self):
        response = None
        if(self.game_matcher.cancel_match(self.params['name'])):
            response = {'status': 'OK', 'reason': 'you cancel the matching'}
        else:
            response = {'status': 'Fail', 'reason': 'Cancel Faild'}
            # shouldn't occur
        return response


    