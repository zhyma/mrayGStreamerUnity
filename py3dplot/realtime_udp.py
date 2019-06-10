import matplotlib.pyplot as plt
import numpy as np
import mpl_toolkits
from mpl_toolkits.mplot3d import Axes3D
from calc3d import rotation, new_axis
from arrow import Arrow3D

from matplotlib import animation
from math import sin, cos, pi

import threading
import time
import socket

import csv

def update(t, input, point, lines):
    o = input.data[0:3]
    point.set_xdata([o[0]])
    point.set_ydata([o[1]])
    # there is no .set_zdata() for 3D data...
    point.set_3d_properties([o[2]])

    axis = new_axis(input.data[3:6])
    for i in range(len(lines)):
        lines[i].set_xdata([o[0], o[0]+axis[i][0]])
        lines[i].set_ydata([o[1], o[1]+axis[i][1]])
        lines[i].set_3d_properties([o[2], o[2]+axis[i][2]])
    return point, lines

class dataThread(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.t = 0
        address = ('127.0.0.1', 8001)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.sendto('request', address)
        # 3 position and 3 rotation
        self.data = [.0, .0, .0, .0, .0, .0]

    def run(self):
        while True:
            buffer, addr = self.sock.recvfrom(2048)
            buffer = buffer.split(',')

            ts = buffer[0]
            print buffer
            self.data = [float(x) for x in buffer[1:4]] + [float(x)*pi/180.0 for x in buffer[4:7]]
            print self.data


if __name__ == '__main__':

    # Attaching 3D axis to the figure

    fig = plt.figure()
    ax = Axes3D(fig)

    ax.view_init(elev=120, azim=-90)
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
    d_thread = dataThread(1, 'dataT')
    d_thread.start()

    # new ax
    axis = new_axis([0, 0, 0])
    lines = []
    lines.append(ax.plot([o[0], o[0] + axis[0][0]], [o[1], o[1] + axis[0][1]], [o[2], o[2] + axis[0][2]])[0])
    lines.append(ax.plot([o[0], o[0] + axis[1][0]], [o[1], o[1] + axis[1][1]], [o[2], o[2] + axis[1][2]])[0])
    lines.append(ax.plot([o[0], o[0] + axis[2][0]], [o[1], o[1] + axis[2][1]], [o[2], o[2] + axis[2][2]])[0])

    point_ani = animation.FuncAnimation(fig, update, frames=np.array([0]), fargs=(d_thread, point, lines),
                                      interval=1, blit=False)

    plt.show()
    print 'done'
