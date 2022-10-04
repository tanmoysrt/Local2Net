import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("localhost", 3000))
data = ""
with open("request.txt", "rb") as f:
    data = f.read()
    f.close()
# data = data.strip().replace("\n", "\r\n")
# data = "GET / HTTP/1.1\r\nHost:localhost"
# data = "GET / HTTP/1.1\r\nHost: localhost\r\nUser-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
data = data + b"\r\n\r\n"
print(data)
sock.send(data)
response = sock.recv(4096)
with open("response.txt", "w") as f:
    f.write(response.decode())
    f.close()
sock.close()
print(response.decode())