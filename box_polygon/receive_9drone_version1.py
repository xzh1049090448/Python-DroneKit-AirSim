import threading
import socket
import time
import math
from dronekit import connect, VehicleMode, LocationGlobalRelative


def receive_pos(num):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('127.0.0.1', 6666))
    while True:
        sock.send(b"1")
        buf = sock.recv(4096)
        # time.sleep(2)
        str1 = str(num) + ":" + buf.decode("ascii") + "\n"
        print(str1)
        if not buf or len(buf) == 0:
            break
        pos = buf.decode("ascii").split(' ')
        try:
            if len(pos) == 2:
                x = float(pos[0]) / 50000 - 35.3632609
                y = float(pos[1]) / 50000 + 149.165230
                if num == 0:
                    str1 = " pos :" + str(x) + "\n" + "," + str(y)
                    print(str1)

        except ValueError:
            pass

    sock.close()


def thread_start():
    th = []
    for i in range(0, 9):
        th.append(threading.Thread(target=receive_pos, args=(i,)))
        th[i].start()


if __name__ == '__main__':
    thread_start()
