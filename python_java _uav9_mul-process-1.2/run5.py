from dronekit import connect, VehicleMode, LocationGlobalRelative
import socket
import time
import math


class Run:

    def __init__(self, id):
        connection_string = '127.0.0.1:14591'
        self.vehicle = connect(connection_string, wait_ready=True)
        self.id = id

    def start(self):
        self.arm_and_takeoff(40)
        self.receive_pos(self.id)

    def arm_and_takeoff(self, aTargetAltitude):
        """武装无人机并飞行至指定高度"""
        # 进行起飞前检查
        print("Basic pre-arm checks")

        while not self.vehicle.is_armable:
            print(" Waiting Copter"  " for vehicle to initialise...")
            time.sleep(1)

        self.vehicle.armed = True

        self.vehicle.mode = VehicleMode("GUIDED")

        while not self.vehicle.armed:
            print(" Waiting for arming...")
            time.sleep(1)

        print("Taking off!")
        aTargetAltitude = aTargetAltitude + 3 * self.id
        self.vehicle.simple_takeoff(aTargetAltitude)

        while True:

            if self.judge_altitude(aTargetAltitude):
                break
            time.sleep(1)
        self.vehicle.airspeed = 4

    def play(self, x1, y1):
        point = LocationGlobalRelative(x1, y1, 40)
        self.vehicle.simple_goto(point)
        for i in range(0, 7):
            if self.judge_pos(x1, y1, self.vehicle):
                break
            time.sleep(1)

    def rad(self, d):
        return (d * math.pi) / 180

    def distance(self, latitude1, longitude1, latitude2, longitude2):
        l1 = self.rad(latitude1)
        l2 = self.rad(latitude2)
        a = l1 - l2
        b = self.rad(longitude1) - self.rad(longitude2)
        s = 2 * math.asin(math.sqrt((math.sin(a / 2) ** 2) + (math.cos(l1) * math.cos(l2) * (math.sin(b / 2) ** 2))))
        s *= 6378137.0
        return s

    def judge_altitude(self, aTargetAltitude):
        sign = 1
        if self.vehicle.location.global_relative_frame.alt < aTargetAltitude * 0.95:
            sign = 0
        if sign == 1:
            return True
        else:
            return False

    def judge_pos(self, x, y, vehicle1):
        """注意经纬度的+-"""
        sign = 0
        print(self.id)
        if self.distance(x, y, vehicle1.location.global_relative_frame.lat,
                         vehicle1.location.global_relative_frame.lon) < 1.1:
            sign = 1

        if sign == 1:
            return True
        else:
            return False

    def receive_pos(self, num):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('127.0.0.1', 6666))
        while True:

            buf = sock.recv(4096)
            print(buf)
            if not buf or len(buf) == 0:
                break
            pos = buf.decode("ascii").split(' ')
            try:

                if len(pos) == 2:
                    x = -float(pos[0]) / 40000 - 35.3632609
                    y = -float(pos[1]) / 40000 + 149.165230

                    self.play(x, y)

                    x1 = -(self.vehicle.location.global_relative_frame.lat + 35.3632609) * 40000
                    y1 = -(self.vehicle.location.global_relative_frame.lon - 149.165230) * 40000
                    str1 = str(x1) + ' ' + str(y1)
                    sock.send(bytes(str1, encoding="utf8"))

            except ValueError:
                pass

        sock.close()
