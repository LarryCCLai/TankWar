class QueryPlayer:
    def __init__(self, PlayerInfoTable, params):
        self.PlayerInfoTable = PlayerInfoTable
        self.params = params

    def execute(self):
        name = self.params['name']
        response = None
        player = self.PlayerInfoTable().select_a_player(name)
        
        
        if len(player) == 1:
            player = player[0]
            response = {'status': 'OK', 'name': player['name']}
        else:
            response = {'status': 'Fail', 'reason': 'The name is not found.'} 
        
        return response