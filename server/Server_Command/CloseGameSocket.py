class CloseGameSocket:
    def __init__(self, PlayerInfoTable, params):
        self.port = params['port']
        self.game_matcher = params['game_matcher']
        
    def execute(self):
        self.game_matcher.close_game_socket(self.port)
        response = {'status': 'OK', 'reason': 'Close Success'}
        return response
    