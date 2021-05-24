#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import threading
import time
from dronekit import connect, VehicleMode, LocationGlobalRelative

# 通过本地的14551端口，使用UDP连接到SITL模拟器
connection_string = '127.0.0.1:14551'
print('Connecting to vehicle on: %s' % connection_string)
# connect函数将会返回一个Vehicle类型的对象，即此处的vehicle
# 即可认为是无人机的主体，通过vehicle对象，我们可以直接控制无人机
vehicle = connect(connection_string, wait_ready=True)

SET = True
lat = []
lon = []
time1 = []
x = [-35.36325170095818, -35.36323175271588, -35.363213857014564, -35.363206061088285, -35.363217535806285, -35.363236564514736, -35.36325432301412, -35.36326200715481, -35.36325170095818]
y = [149.1652404053844, 149.1652283103651, 149.16524300118357, 149.16526612215125, 149.16528784685437, 149.16529731915222, 149.16528329236465, 149.16525993169373, 149.1652404053844]
z = 7
delay = 4.5


# 定义arm_and_takeoff函数，使无人机解锁并起飞到目标高度
# 参数aTargetAltitude即为目标高度，单位为米
def arm_and_takeoff(aTargetAltitude):
    # 进行起飞前检查
    print("Basic pre-arm checks")
    # vehicle.is_armable会检查飞控是否启动完成、有无GPS fix、卡曼滤波器
    # 是否初始化完毕。若以上检查通过，则会返回True
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)

    # 解锁无人机（电机将开始旋转）
    print("Arming motors")
    vehicle.armed = True
    # 将无人机的飞行模式切换成"GUIDED"（一般建议在GUIDED模式下控制无人机）
    vehicle.mode = VehicleMode("GUIDED")
    # 通过设置vehicle.armed状态变量为True，解锁无人机
    # 在无人机起飞之前，确认电机已经解锁
    while not vehicle.armed:
        print(" Waiting for arming...")
        vehicle.armed = True
        time.sleep(1)

    # 发送起飞指令
    print("Taking off!")
    # simple_takeoff将发送指令，使无人机起飞并上升到目标高度
    vehicle.simple_takeoff(aTargetAltitude)

    # 在无人机上升到目标高度之前，阻塞程序
    while True:
        print(" Altitude: ", vehicle.location.global_relative_frame.alt)
        # 当高度上升到目标高度的0.95倍时，即认为达到了目标高度，退出循环
        # vehicle.location.global_relative_frame.alt为相对于home点的高度
        if vehicle.location.global_relative_frame.alt >= aTargetAltitude * 0.95:
            print("Reached target altitude")
            break
        # 等待1s
        time.sleep(1)
    vehicle.airspeed = 1
    point1 = LocationGlobalRelative(x[0], y[0], z)
    vehicle.simple_goto(point1)
    time.sleep(delay + 7)


def play():
    global SET

    point = []
    for i in range(1, 9):
        point.append(LocationGlobalRelative(x[i], y[i], z))
        vehicle.simple_goto(point[i-1])
        if i == 8:
            time.sleep(delay)
        time.sleep(delay)
    # 发送"返航"指令
    time.sleep(delay+5)
    SET = False

    vehicle.mode = VehicleMode("RTL")
    vehicle.close()


def draw_points():
    global SET
    while SET:
        lat.append(vehicle.location.global_relative_frame.lat)
        lon.append(vehicle.location.global_relative_frame.lon)
        time1.append(time.perf_counter())
        time.sleep(1)
    print(lat)
    print(lon)
    print(time1)


if __name__ == '__main__':
    arm_and_takeoff(10)
    threads = [threading.Thread(target=play),
               threading.Thread(target=draw_points)]
    for t in threads:
        # 启动线程
        t.start()

