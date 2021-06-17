from Server_Command.QueryPlayer import QueryPlayer
from Server_Command.SignUp import SignUp
from Server_Command.SignIn import SignIn
from Server_Command.Play_Cancel import Play
from Server_Command.Play_Cancel import Cancel
from Server_Command.Update import Update
from DB.PlayerInfoTable import PlayerInfoTable

command_dict = {
    'sign_up': SignUp,
    'sign_in': SignIn,
    'query': QueryPlayer,
    'play': Play,
    'cancel': Cancel,
    'update': Update,
}

class JobDispatcher:
    def execute(self, command, params):
        proc_ret = command_dict[command](PlayerInfoTable, params).execute()
        return proc_ret