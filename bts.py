import socket
from math import sqrt
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(("challenge01.root-me.org", 52002))
    data = s.recv(1024)
    goodline = data.decode().splitlines()[-1]
    nbr1 = int(goodline.split(' ')[5])
    nbr2 = int(goodline.split(' ')[9])
    s.sendall(f"{round(sqrt(nbr1)*nbr2, 2)}\n".encode())
    data = s.recv(1024)
    print(data.decode())