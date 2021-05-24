import threading
import time
import math
from dronekit import connect, VehicleMode, LocationGlobalRelative

"""
全局变量设置 0 到9 阻塞控制每个无人机到一个点同时去下一个点
"""
vehicle = []
ACCOUNT1 = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
position = []
UAV_num = 9
position_txt = '中间人1-1.txt'


def connection():
    """连接飞机"""
    connection_string = [
        '127.0.0.1:14551',
        '127.0.0.1:14561',
        '127.0.0.1:14571',
        '127.0.0.1:14581',
        '127.0.0.1:14591',
        '127.0.0.1:14601',
        '127.0.0.1:14611',
        '127.0.0.1:14621',
        '127.0.0.1:14631',
        '127.0.0.1:14641',
    ]
    for i in range(0, UAV_num):
        vehicle.append(connect(connection_string[i], wait_ready=True))


def arm_and_takeoff(aTargetAltitude):
    """武装无人机并飞行至指定高度"""

    print("Basic pre-arm checks")
    for i in range(0, UAV_num):
        while not vehicle[i].is_armable:
            print(" Waiting Copter" + str(i) + " for vehicle to initialise...")
            time.sleep(1)

    print("All copter arming motors")
    for i in range(0, UAV_num):
        vehicle[i].armed = True
        vehicle[i].mode = VehicleMode("GUIDED")

    for i in range(0, UAV_num):
        while not vehicle[i].armed:
            print(" Waiting for arming...")
            time.sleep(1)

    for i in range(0, UAV_num):
        TargetAltitude = aTargetAltitude + 3 * i
        vehicle[i].simple_takeoff(TargetAltitude)

    while True:
        if judge_altitude(aTargetAltitude):
            break
        time.sleep(1)

    for i in range(0, UAV_num):
        vehicle[i].airspeed = 6


def rad(d):
    return (d * math.pi) / 180


def distance(latitude1, longitude1, latitude2, longitude2):
    l1 = rad(latitude1)
    l2 = rad(latitude2)
    a = l1 - l2
    b = rad(longitude1) - rad(longitude2)
    s = 2 * math.asin(math.sqrt((math.sin(a / 2) ** 2) + (math.cos(l1) * math.cos(l2) * (math.sin(b / 2) ** 2))))
    s *= 6378137.0
    return s


def judge_altitude(aTargetAltitude):
    sign = 1
    for i in range(0, UAV_num):
        TargetAltitude = aTargetAltitude + 3 * i
        if vehicle[i].location.global_relative_frame.alt < TargetAltitude * 0.95:
            sign = 0
    if sign == 1:
        return True
    else:
        return False


def judge_pos(x, y, vehicle1):
    """注意经纬度的+-"""
    sign = 0
    if distance(x, y, vehicle1.location.global_relative_frame.lat, vehicle1.location.global_relative_frame.lon) < 1:
        sign = 1

    if sign == 1:
        return True
    else:
        return False


def play(x1, y1, num):
    global ACCOUNT1

    while ACCOUNT1[num] == 0:
        pass

    ACCOUNT1[num] = ACCOUNT1[num] - 1
    point = LocationGlobalRelative(x1, y1, 40)
    vehicle[num].simple_goto(point)

    for i in range(0, 5):
        if judge_pos(x1, y1, vehicle[num]):
            break
        time.sleep(1)

    for i in range(0, UAV_num):
        if ACCOUNT1[i] == 1:
            return
    for i in range(0, UAV_num):
        ACCOUNT1[i] = 1


def receive_pos(num, pos):
    global ACCOUNT1

    for buf in pos:
        if not buf or len(buf) == 0:
            break
        pos = buf.split(' ')
        try:
            if len(pos) == 2:
                x = -float(pos[0]) / 50000 - 35.3632609
                y = -float(pos[1]) / 50000 + 149.165230
                play(x, y, num)
        except ValueError:
            pass

    print("over!")


def read_text():
    for num in range(0, UAV_num):
        lnum = 0
        temp = []
        with open(position_txt, 'r') as fd:
            for line in fd:
                lnum += 1
                if lnum % UAV_num == num:
                    temp.append(line[:-1])
        fd.close()
        position.append(temp)


def thread_start():
    th = []
    for i in range(0, UAV_num):
        th.append(threading.Thread(target=receive_pos, args=(i, position[i],)))
        th[i].start()


if __name__ == '__main__':
    read_text()
    connection()
    arm_and_takeoff(40)
    thread_start()
