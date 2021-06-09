from SocketServer import SocketServer


from DB.DBConnection import DBConnection
from DB.DBInitializer import DBInitializer

host = "127.0.0.1"
port = 20001
accept_num = 10
DBConnection.db_file_path = "../example.db"

if __name__ == '__main__':
    
    DBInitializer().execute()
    

    server = SocketServer(host, port, accept_num)
    server.setDaemon(True)
    server.serve()

    # because we set daemon is true, so the main thread has to keep alive
    while True:
        command = input()
        if command == "finish":
            break
    
    
    server.server_socket.close()
    print("leaving ....... ")
