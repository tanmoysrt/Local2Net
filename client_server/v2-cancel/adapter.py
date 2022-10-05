import socket
from queue import Queue
import threading


class Adapter:
    def __init__(self) -> None:
        self.system_host = "127.0.0.1"
        self.system_port = "8080"

        self.client_host = "127.0.0.1"
        self.client_port = "3000"

        self.buffer = Queue() 

        self.killed = False

    def start_server(self): 
        # Build socket connection
        system_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        system_sock.connect((self.system_host, int(self.system_port)))


        self.system_sock = system_sock

        # Start threads
        self.system_receiver_thread = threading.Thread(target=self.system_receive_thread)
        self.system_sender_thread = threading.Thread(target=self.system_send_thread)

        self.system_receiver_thread.start()
        self.system_sender_thread.start()

        self.system_receiver_thread.join()
        self.system_sender_thread.join()


    # Data receiving thread from system
    def system_receive_thread(self):
        while True:
            data = self.system_sock.recv(4096)
            if not data:
                print("Invalid data received from system")
                break
            self.buffer.put(data)
            print("SYSTEM --> ADAPTER : "+data.decode())

    # Data sending thread to systme
    def system_send_thread(self):
        while True:
            # if self.buffer.empty():
            #     sleep(0.01)
            data = input("Enter data to send to system: ")
            self.system_sock.sendall(data.encode())
            print("ADAPTER --> SYSTEM : "+data)

    def close(self):
        self.killed = True
        self.system_sock.close()

# Driver code
if __name__ == "__main__":
    adapter = Adapter()
    adapter.start_server()
    adapter.close()