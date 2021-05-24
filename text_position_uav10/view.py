import numpy as np
from matplotlib import pyplot as plt
from scipy.interpolate import make_interp_spline

"""
蓝的是ardupilot 实线
橙的是simpleflight 虚线
"""
position = []
X = []
Y = []


def read_text():
    for num in range(0, 10):
        lnum = 0
        temp = []
        with open('position.txt', 'r') as fd:
            for line in fd:
                lnum += 1
                if lnum % 10 == num:
                    temp.append(line[:-1])
        fd.close()
        position.append(temp)
    for i in range(0, 10):
        tempx = []
        tempy = []
        for buf in position[i]:
            pos = buf.split(' ')
            x = -float(pos[0])
            y = -float(pos[1])
            tempx.append(x)
            tempy.append(y)
        # print(tempx)
        X.append(np.array(tempx))
        Y.append(np.array(tempy))


read_text()
for i in range(0, 10):
    # print(X[i])
    # print(Y)
    plt.plot(X[i], Y[i])
plt.xlabel("X")  # X轴标题及字号
plt.ylabel("Y")  # Y轴标题及字号
plt.show()
