import socket
from queue import Queue
import threading
from time import sleep


class Server:
    def __init__(self) -> None:
        self.host = "127.0.0.1"
        self.port = "8080"

        self.client_host = "127.0.0.1"
        self.client_port = "3000"

        self.buffer = Queue()

        self.killed = False

    def start_server(self):
        # Build socket connection
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, int(self.port)))
        self.sock.listen()


    def close(self):
        self.killed = True
        self.sock.close()

# Driver code