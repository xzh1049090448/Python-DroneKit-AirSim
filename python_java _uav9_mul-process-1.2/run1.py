import time
from dronekit import LocationGlobalRelative, Attitude
import run


class Run(run.Run):

    def __init__(self, id):
        self.connection_string = '127.0.0.1:14551'
        self.id = id

    # def play(self, x1, y1):
    #     point = LocationGlobalRelative(x1, y1, 40)
    #     self.vehicle.simple_goto(point)
    #     print(self.vehicle.attitude)
    #     for i in range(0, 1):
    #         if self.judge_pos(x1, y1, self.vehicle):
    #             break
    #         time.sleep(1)