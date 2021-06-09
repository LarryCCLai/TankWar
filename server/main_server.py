from SocketServer import SocketServer
from JobDispatcher import JobDispatcher

from DB.DBConnection import DBConnection
from DB.DBInitializer import DBInitializer

host = "127.0.0.1"
port = 20001
accept_num = 10
DBConnection.db_file_path = "../example.db"

if __name__ == '__main__':
    
    DBInitializer().execute()
    job_dispatcher = JobDispatcher()

    server = SocketServer(host, port, accept_num)
    server.set_job_dispatcher(job_dispatcher)
    server.setDaemon(True)
    server.serve()

    # because we set daemon is true, so the main thread has to keep alive
    while True:
        command = input()
        if command == "finish":
            break
    
    
    server.server_socket.close()
    print("leaving ....... ")
