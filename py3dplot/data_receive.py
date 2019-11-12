import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from tool.calc3d import rotation, new_axis
from tool.arrow import Arrow3D

from matplotlib import animation
from math import sin, cos, pi

import threading
import time
import socket

from datetime import datetime

def update(t, input, point, lines):
    o = input.data[0:3]
    point.set_xdata([o[0]])
    point.set_ydata([o[1]])
    # there is no .set_zdata() for 3D data...
    point.set_3d_properties([o[2]])

    pitch = -input.data[5]
    yaw = input.data[3]
    roll =  -input.data[4]+pi/2
    axis = new_axis([roll, pitch, yaw])

    for i in range(len(lines)):
        lines[i].set_xdata([o[0], o[0]+axis[i][0]])
        lines[i].set_ydata([o[1], o[1]+axis[i][1]])
        lines[i].set_3d_properties([o[2], o[2]+axis[i][2]])

    return point, lines

class dataThread(threading.Thread):
    def __init__(self, threadID, name, ip_addr):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.t = 0
        address = (ip_addr, 8001)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.sendto('request', address)
        # 3 position and 3 rotation
        self.data = [.0, .0, .0, .0, .0, .0]
        # datetime object containing current date and time
        now = datetime.now()
        print("now =", now)
        # dd/mm/YY H:M:S
        dt_string = now.strftime("%m_%d__%H_%M")
        print("date and time =", dt_string)
        # self.file = open(dt_string + '.csv', 'w')

    def run(self):
        print 'recording data'
        while True:
            buffer, addr = self.sock.recvfrom(2048)
            # self.file.write(buffer + '\n')
            buffer = buffer.split(',')

            ts = buffer[0]
            #print buffer
            self.data = [float(x) for x in buffer[1:4]] + [float(x)*pi/180.0 for x in buffer[4:7]]
            print int(float(buffer[4])), ', ', int(float(buffer[5])), ',', int(float(buffer[6]))
            #print self.data


if __name__ == '__main__':
    # Attaching 3D axis to the figure
    fig = plt.figure()
    ax = Axes3D(fig)

    ax.view_init(elev=19, azim=-148)
    ax.set_xlim3d(-1, 1)
    ax.set_ylim3d(-1, 1)
    ax.set_zlim3d(-1, 1)

    a = Arrow3D([0, 1], [0, 0], [0, 0], mutation_scale=20, lw=3, arrowstyle="-|>", color="r")
    ax.text(1, 0, 0, 'x', fontsize=30)
    ax.add_artist(a)
    a = Arrow3D([0, 0], [0, 1], [0, 0], mutation_scale=20, lw=3, arrowstyle="-|>", color="r")
    ax.text(0, 1, 0, 'y', fontsize=30)
    ax.add_artist(a)
    a = Arrow3D([0, 0], [0, 0], [0, 1], mutation_scale=20, lw=3, arrowstyle="-|>", color="r")
    ax.text(0, 0, 1, 'z', fontsize=30)
    ax.add_artist(a)

    # origin
    o = [0, 0, 0]
    point = ax.plot([o[0]], [o[1]], [o[2]], 'k.', markersize=12)[0]
    d_thread = dataThread(1, 'dataT', '130.215.206.182')
    d_thread.start()

    # new ax
    axis = new_axis([0, 0, 0])
    lines = []
    lines.append(ax.plot([o[0], o[0] + axis[0][0]], [o[1], o[1] + axis[0][1]], [o[2], o[2] + axis[0][2]], color='r')[0])
    lines.append(ax.plot([o[0], o[0] + axis[1][0]], [o[1], o[1] + axis[1][1]], [o[2], o[2] + axis[1][2]], color='g')[0])
    lines.append(ax.plot([o[0], o[0] + axis[2][0]], [o[1], o[1] + axis[2][1]], [o[2], o[2] + axis[2][2]], color='b')[0])

    point_ani = animation.FuncAnimation(fig, update, frames=np.array([0]), fargs=(d_thread, point, lines),
                                      interval=1, blit=False)

    plt.show()
    print 'done'
