import socket
import threading

adapter_conn = None
adapter_addr = None
client_conn = None
client_addr = None


def main():
    global adapter_conn
    global adapter_addr
    global client_conn
    global client_addr
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    sock.bind(("127.0.0.1", 8005))
    sock.listen(1)

    adapter_conn, adapter_addr = sock.accept()
    print("Connected adapter : ", adapter_addr)

    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    client_sock.bind(("127.0.0.1", 3002))
    client_sock.listen(1)

    client_conn, client_addr = client_sock.accept()
    print("Connected client : ", client_addr)

    thread1 = threading.Thread(target=thread1_func)
    thread2 = threading.Thread(target=thread2_func)

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()


def thread1_func():
    global adapter_conn
    global adapter_addr
    global client_conn
    global client_addr
    while True:
        try:
            data = adapter_conn.recv(1024)
            print("Received data from adapter : ", data)
            client_conn.sendall(data)
        except:
            print("Error while receiving data from adapter")
            break

def thread2_func():
    global adapter_conn
    global adapter_addr
    global client_conn
    global client_addr
    while True:
        try:
            data = client_conn.recv(1024)
            print("Received data from client : ", data)
            adapter_conn.sendall(data)
        except:
            print("Error while receiving data from client")
            break

if __name__ == "__main__":
    main()