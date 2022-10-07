# server.py
import time
import socket
import sys

print("\nWelcome to Chat Room\n")
print("Initialising....\n")
time.sleep(1)

s = socket.socket()
host = input(str("Enter ip address: "))
port = int(input("Enter port number: "))
s.bind((host, port))
s.listen(1)
s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, True)


print("\nWaiting for incoming connections...\n")
conn, addr = s.accept()
print("Received connection from ", addr[0], "(", addr[1], ")\n")


while True:
    message = input(str("Me : "))
    if message == "[e]":
        message = "Left chat room!"
        conn.send(message.encode())
        print("\n")
        break
    conn.send(message.encode())
    message = conn.recv(1024)
    message = message.decode()
    print("Received : ", message)