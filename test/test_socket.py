import threading
import socket
import time
from dronekit import connect, VehicleMode, LocationGlobalRelative


def receive_pos():
    global x
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # sock.connect(('10.16.51.83', 55533))
    sock.connect(('10.16.51.83', 6666))
    print("ssssssss")
    # sock.send(b"open\s+data\s+data\s+")
    buf = ''
    # print("-----------")
    print("sssssswsss")
    while True:
        # print("-----sd------")
        buf = sock.recv(4096)
        print("ssssssss")
        if not buf or len(buf) == 0:
            break
        print()
        pos = buf.decode("ascii").split(",")
        print(pos)
        while "" in pos:
            pos.remove("")
        print(pos)
        for i in range(0, len(pos), 2):
            x = int(pos[i])
            y = int(pos[i + 1])
            print("x=", x, "y=", y)
            th = []
            for j in range(0, 9):
                print("-------", i, "---------")
                with open("text" + str(j), 'w', encoding='utf-8') as f:
                    f.write(str(x) + " " + str(y) + '\n')

    # print("-----8888888888  ------")
    sock.close()


if __name__ == '__main__':
    receive_pos()
