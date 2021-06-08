class SignIn:
    def __init__(self, PlayerInfoTable, params):
        self.PlayerInfoTable = PlayerInfoTable
        self.params = params

    def execute(self):
        name = self.params['name']
        password = self.params['password']
        response = None
        
        player = self.PlayerInfoTable().select_a_player(name)
        
        if(len(player) == 1):
            player = player[0]
            if(name != player['name']):
                response = {'status': 'Fail', 'reason': 'The name is not found.'}  
            elif(password != player['password']):
                response = {'status': 'Fail', 'reason': 'Wrong password'}
            else:
                player_info = {'name': player['name'], 'win':player['win'], 'loss':player['loss']}
                response = {'status': 'OK', 'reason': 'Name and password match', 'player_info': player_info}
        else:
            response = {'status': 'Fail', 'reason': 'The name is not found.'}  
        return response
        