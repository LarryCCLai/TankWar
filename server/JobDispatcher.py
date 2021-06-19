from Server_Command.QueryPlayer import QueryPlayer
from Server_Command.SignUp import SignUp
from Server_Command.SignIn import SignIn
from Server_Command.Play import Play
from Server_Command.Cancel import Cancel
from Server_Command.Update import Update
from Server_Command.CloseGameSocket import CloseGameSocket
from DB.PlayerInfoTable import PlayerInfoTable
from GameMatcher import GameMatcher


command_dict = {
    'sign_up': SignUp,
    'sign_in': SignIn,
    'query': QueryPlayer,
    'play': Play,
    'cancel': Cancel,
    'update': Update,
    'close_game_socket': CloseGameSocket,

}

class JobDispatcher:
    def __init__(self):
        self.game_matcher = GameMatcher()
    def execute(self, command, params):
        if(command=='play' or command == ' cancel' or command == 'close_game_socket'):
            params['game_matcher'] = self.game_matcher
        proc_ret = command_dict[command](PlayerInfoTable, params).execute()
        return proc_ret