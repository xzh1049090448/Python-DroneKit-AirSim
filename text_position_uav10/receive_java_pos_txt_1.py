import threading
import socket
import time
from dronekit import connect, VehicleMode, LocationGlobalRelative


def receive_pos(num):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('127.0.0.1', 6666))
    buf = ''
    while True:
        sock.send(b"1")
        buf = sock.recv(4096)
        if num == 0:
            print(buf)
        if not buf or len(buf) == 0:
            break
        pos = buf.decode("ascii").split(' ')
        try:
            if len(pos) == 2:
                x = float(pos[0])
                y = float(pos[1])
                with open("text_pos.txt", 'a', encoding='utf-8') as f:
                    f.write(str(x) + " " + str(y) + '\n')
                f.close()
        except ValueError:
            pass
    # print("-----8888888888  ------")
    sock.close()


if __name__ == '__main__':
    th = []
    for i in range(0, 9):
        th.append(threading.Thread(target=receive_pos, args=(i,)))
        th[i].start()
