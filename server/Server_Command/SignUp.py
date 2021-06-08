class SignUp:
    def __init__(self, PlayerInfoTable, params):
        self.PlayerInfoTable = PlayerInfoTable
        self.params = params

    def execute(self):
        self.PlayerInfoTable().insert_a_player(self.params)
        return {'status': 'OK'} 