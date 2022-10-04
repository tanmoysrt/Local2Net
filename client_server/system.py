import socket
from time import sleep

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 3001  # Port to listen on (non-privileged ports are > 1023)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        request = ""
        while True:
            data = conn.recv(1024).decode()
            if data == "":
                break
            if not data:
                break
            request += data
        
        with open("request.txt", "wb") as f:
            f.write(bytes(request, 'utf-8'))
            f.close()
        sleep(10)
        print("Request received")
        with open("response.txt", "r") as f:
            print(f.read())
            f.close()
        
except KeyboardInterrupt:
    print("Exiting...")
    s.close()