class SignIn:
    def __init__(self, PlayerInfoTable, params):
        self.PlayerInfoTable = PlayerInfoTable
        self.params = params

    def execute(self):
        name = self.params['name']
        password = self.params['password']
        response = None
        
        player = self.PlayerInfoTable().login_check(name, password)
        
        if(len(player) == 1): #identify checked
            player = player[0]
            player_info = {'name': player['name'], 'win':player['win'], 'loss':player['loss']}
            response = {'status': 'OK', 'reason': 'Name and password match', 'player_info': player_info}
        else:
            response = {'status': 'Fail', 'reason': 'Please check your login info.'}  
        return response
        