import socket
import base64

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(("challenge01.root-me.org", 52023))
    data = s.recv(1024)
    enc = data.decode().splitlines()[-1].split("'")[1]
    s.sendall(base64.b64decode(enc))
    s.sendall('\n'.encode())
    data = s.recv(1024)
    print(data.decode())