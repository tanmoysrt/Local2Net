# client.py
import time
import socket
import sys

print("\nWelcome to Chat Room\n")
print("Initialising....\n")
time.sleep(1)

s = socket.socket()

host = input(str("Enter server address: "))
port = int(input("Enter port number: "))

name = input(str("\nEnter your name: "))
print("\nTrying to connect to ", host, "(", port, ")\n")
time.sleep(1)
s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, True)

s.connect((host, port))
print("Connected...\n")

s.send(name.encode())
s_name = s.recv(1024)
s_name = s_name.decode()
print(s_name, "has joined the chat room\nEnter [e] to exit chat room\n")

while True:
    message = s.recv(1024)
    message = message.decode()
    print(s_name, ":", message)
    message = input(str("Me : "))
    if message == "[e]":
        message = "Left chat room!"
        s.send(message.encode())
        print("\n")
        break
    s.send(message.encode())
