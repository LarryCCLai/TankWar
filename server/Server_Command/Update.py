class Update:
    def __init__(self, PlayerInfoTable, params):
        self.PlayerInfoTable = PlayerInfoTable
        self.params = params
    
    def execute(self):
        name = self.params['name']
        result = self.params['result']
        if result == 'win':
            winner = self.PlayerInfoTable().select_a_player(name)[0]
            self.PlayerInfoTable().update_a_player(winner['name'], winner['win']+1, winner['loss'])
        else:
            loser = self.PlayerInfoTable().select_a_player(name)[0]
            self.PlayerInfoTable().update_a_player(loser['name'], loser['win'], loser['loss']+1)

        response = {'status': 'OK', 'reason': 'Update success.'}

        return response