from threading import Thread
import socket
import json
import time

class GameSocket(Thread):
    def __init__(self, host, port, accept_num=2):
        super().__init__()

        self.client_list = []
        
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((host, port))
        self.server_socket.listen(accept_num)

    def serve(self):
        self.start()

    def run(self):
        while True:
            connection, address = self.server_socket.accept()
            self.client_list.append((address, connection))
            
            print("{} connected".format(address))

            self.new_connection(connection=connection,
                                address=address)

    def new_connection(self, connection, address):
        Thread(target=self.receive_message_from_client,
               kwargs={
                   "connection": connection,
                   "address": address}, daemon=True).start()

    def receive_message_from_client(self, connection, address):
        keep_going = True
        while keep_going:
            try:
                message = connection.recv(1024).strip().decode()
            except:
                keep_going = False
            else:
                if not message:
                    break

                message = json.loads(message)

                idx = self.find_other(address)
                print(self.client_list[idx][0])
                print(message)
                print('  server received: {} form {}'.format(message, address))
                
                if message['command'] == "close":
                    connection.send("closing".encode())
                    break
                else:
                    self.client_list[idx][1].send(json.dumps(message).encode())

        connection.close()
        print("close connection")
    
    def find_other(self, address):
        print('address: ',address[1])
        print('client_list', self.client_list)
        if(address[1] == self.client_list[0][0][1]):
            return 1
        return 0