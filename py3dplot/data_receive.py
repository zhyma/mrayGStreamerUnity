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

if __name__ == '__main__':
    plt.ion()
    # Attaching 3D axis to the figure
    fig = plt.figure()
    ax = Axes3D(fig)

    ax.view_init(elev=19, azim=-148)
    ax.set_xlim3d(-3, 3)
    ax.set_ylim3d(-3, 3)
    ax.set_zlim3d(-3, 3)

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
    data = [.0, .0, .0, .0, .0, .0]

    # new ax
    axis = new_axis([0, 0, 0])
    lines = []
    #frame for the camera/head, right controller, left controller
    for i in range(3):
        lines.append(ax.plot([o[0], o[0] + axis[0][0]], [o[1], o[1] + axis[0][1]], [o[2], o[2] + axis[0][2]], color='r')[0])
        lines.append(ax.plot([o[0], o[0] + axis[1][0]], [o[1], o[1] + axis[1][1]], [o[2], o[2] + axis[1][2]], color='g')[0])
        lines.append(ax.plot([o[0], o[0] + axis[2][0]], [o[1], o[1] + axis[2][1]], [o[2], o[2] + axis[2][2]], color='b')[0])


    address = ("127.0.0.1", 23023)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto('request', address)
    # 3 position and 3 rotation
    

    while True:
        try:
            sock.settimeout(1)
            buffer, addr = sock.recvfrom(2048)
            buffer = buffer.split(',')

            # print buffer
            ts = buffer[0]
            
            data = [float(x) for x in buffer[1:4]] + [float(x)*pi/180.0 for x in buffer[4:7]]
            offset = 7
            data += [float(x) for x in buffer[offset+1:offset+4]] + [float(x)*pi/180.0 for x in buffer[offset+4:offset+7]]
            offset = 14
            data += [float(x) for x in buffer[offset+1:offset+4]] + [float(x)*pi/180.0 for x in buffer[offset+4:offset+7]]

            for i in [0,1,2]:
                if data[i*6:i*6+3]==[0.0, 0.0, 0.0]:
                    continue
                [x, y, z, roll, pitch, yaw] = data[i*6:i*6+6]

                point.set_xdata([x])
                point.set_ydata([y])
                # there is no .set_zdata() for 3D data...
                point.set_3d_properties([z])

                axis = new_axis([roll, pitch, yaw])
                if i > 0:
                    axis = [l/2 for l in axis]

                # three axis from
                for j in [0,1,2]:
                    lines[i*3+j].set_xdata([x, x+axis[j][0]])
                    lines[i*3+j].set_ydata([y, y+axis[j][1]])
                    lines[i*3+j].set_3d_properties([z, z+axis[j][2]])

            fig.canvas.draw()
            fig.canvas.flush_events()
        except:
            print "no server detected, reconnecting"
            time.sleep(0.5)
            sock.sendto('request', address)

