import threading
import socket
import time
import math
from dronekit import connect, VehicleMode, LocationGlobalRelative

"""
全局变量设置 0 到9 阻塞控制每个无人机到一个点同时去下一个点
"""
vehicle = []
ACCOUNT1 = [1, 1, 1, 1, 1, 1, 1, 1, 1]
ACCOUNT2 = [1, 1, 1, 1, 1, 1, 1, 1, 1]


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
    ]
    for i in range(0, 9):
        vehicle.append(connect(connection_string[i], wait_ready=True))


def arm_and_takeoff(aTargetAltitude):
    """武装无人机并飞行至指定高度"""
    # 进行起飞前检查
    print("Basic pre-arm checks")
    # vehicle.is_armable会检查飞控是否启动完成、有无GPS fix、卡曼滤波器
    # 是否初始化完毕。若以上检查通过，则会返回True
    for i in range(0, 9):
        while not vehicle[i].is_armable:
            print(" Waiting Copter" + str(i) + " for vehicle to initialise...")
            time.sleep(1)
            # 解锁无人机（电机将开始旋转）

    print("All copter arming motors")
    for i in range(0, 9):
        vehicle[i].armed = True
        # 将无人机的飞行模式切换成"GUIDED"（一般建议在GUIDED模式下控制无人机）
        vehicle[i].mode = VehicleMode("GUIDED")
        # 通过设置vehicle.armed状态变量为True，解锁无人机
        # 在无人机起飞之前，确认电机已经解锁
    for i in range(0, 9):
        while not vehicle[i].armed:
            print(" Waiting for arming...")
            time.sleep(1)

    # 发送起飞指令
    print("Taking off!")
    # simple_takeoff将发送指令，使无人机起飞并上升到目标高度
    for i in range(0, 9):
        vehicle[i].simple_takeoff(aTargetAltitude + 2 * i)

    # 在无人机上升到目标高度之前，阻塞程序
    while True:
        # print(" Altitude: ", vehicle.location.global_relative_frame.alt)
        # 当高度上升到目标高度的0.95倍时，即认为达到了目标高度，退出循环
        # vehicle.location.global_relative_frame.alt为相对于home点的高度
        if judge_altitude(aTargetAltitude):
            print("Reached target altitude")
            break
        # 等待1s
        time.sleep(1)
    for i in range(0, 9):
        vehicle[i].airspeed = 3


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
    for i in range(0, 9):
        if vehicle[i].location.global_relative_frame.alt < aTargetAltitude * 0.95:
            sign = 0
    if sign == 1:
        return True
    else:
        return False


def judge_pos(x, y, vehicle1):
    """注意经纬度的+-"""
    sign = 0
    # print(distance(x, y, vehicle1.location.global_relative_frame.lat, vehicle1.location.global_relative_frame.lon))
    if distance(x, y, vehicle1.location.global_relative_frame.lat, vehicle1.location.global_relative_frame.lon) < 1:
        sign = 1

    if sign == 1:
        return True
    else:
        return False


def play(x1, y1, num):
    global ACCOUNT1, ACCOUNT2

    while ACCOUNT1[num] == 0:
        pass

    ACCOUNT1[num] = ACCOUNT1[num] - 1
    # 设置无人机空速
    # LocationGlobalRelative是一个类，它由经纬度(WGS84)和相对于home点的高度组成
    point = LocationGlobalRelative(x1, y1, 40)
    # if i == 0:
    #     print(vehicle[i].location.global_relative_frame.lat)d
    # print(point)
    vehicle[num].simple_goto(point)
    # simple_goto函数只发送指令，不判断有没有到达目标航点
    # 它可以被其他后续指令打断，此处延时

    while True:
        # print("real:", vehicle[i].location.global_relative_frame.lat)
        # print(i)
        # n = n - 1
        if judge_pos(x1, y1, vehicle[num]):
            # print("Reached target pos")
            break
        # 等待1s

    for i in range(0, 9):
        if ACCOUNT1[i] == 1:
            return
    for i in range(0, 9):
        ACCOUNT1[i] = 1
    # 空速 + 风速 = 地速（顺风）
    # 空速 - 风速 = 地速（逆风）


def receive_pos(num):
    global ACCOUNT1, ACCOUNT2
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('127.0.0.1', 6666))
    # sock.connect(('10.16.51.83', 6666))
    # last_x = float
    # last_y = float
    while True:
        sock.send(b"1")
        buf = sock.recv(4096)
        if num == 0:
            print(buf)
        if not buf or len(buf) == 0:
            break
        pos = buf.decode("ascii").split(' ')
        try:
            # time.sleep(1)
            # while ACCOUNT1[num] == 0:
            #     time.sleep(1)
            # ACCOUNT1[num] = ACCOUNT1[num] - 1
            if len(pos) == 2:
                x = float(pos[0]) / 50000 - 35.3632609
                y = float(pos[1]) / 50000 + 149.165230
                # if num == 0:
                #     str1 = " pos :" + str(x) + "\n" + "," + str(y)
                #     print(str1)
                play(x, y, num)
                # time.sleep(10)
                # if num == 0:
                #     for i in range(0, 9):
                #         while ACCOUNT1[i] == 1:
                #             pass
                #     for i in range(0, 9):
                #         ACCOUNT1[i] = 1
                # last_x = x
                # last_y = y

        except ValueError:
            pass

        # for i in range(0, 9):
        #     if ACCOUNT1[i] == 1:
        #         return
        # for i in range(0, 9):
        #     ACCOUNT1[i] = 1

    sock.close()


def thread_start():
    th = []
    for i in range(0, 9):
        th.append(threading.Thread(target=receive_pos, args=(i,)))
        th[i].start()


if __name__ == '__main__':
    connection()
    arm_and_takeoff(40)
    thread_start()
