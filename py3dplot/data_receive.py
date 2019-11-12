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
    # three frames
    while input.lock==True:
        time.sleep(5)
    input.lock = True
    data = list(input.data)
    input.lock = False
    for i in [0,1,2]:
        if data[i*6:i*6+3]==[0.0, 0.0, 0.0]:
            continue
        [x, z, y] = data[i*6:i*6+3]
        print [x, y, z]
        
        # point.set_xdata([o[0]])
        # point.set_ydata([o[1]])
        # # there is no .set_zdata() for 3D data...
        # point.set_3d_properties([o[2]])

        point.set_xdata([x])
        point.set_ydata([y])
        # there is no .set_zdata() for 3D data...
        point.set_3d_properties([z])

        pitch = -data[i*6+5]
        yaw = data[i*6+3]
        roll =  -data[i*6+4]+pi/2
        axis = new_axis([roll, pitch, yaw])
        if i > 0:
            axis = [l/2 for l in axis]

        # three axis from
        for j in [0,1,2]:
            lines[i*3+j].set_xdata([x, x+axis[j][0]])
            lines[i*3+j].set_ydata([y, y+axis[j][1]])
            lines[i*3+j].set_3d_properties([z, z+axis[j][2]])

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
        self.lock = False
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

            # print buffer
            ts = buffer[0]
            
            # thread lock is only used for sync with Matplotlib. Remove if you directly publish it to ROS
            while self.lock==True:
                time.sleep(5)
            self.lock = True
            self.data = [float(x) for x in buffer[1:4]] + [float(x)*pi/180.0 for x in buffer[4:7]]
            offset = 7
            self.data += [float(x) for x in buffer[offset+1:offset+4]] + [float(x)*pi/180.0 for x in buffer[offset+4:offset+7]]
            offset = 14
            self.data += [float(x) for x in buffer[offset+1:offset+4]] + [float(x)*pi/180.0 for x in buffer[offset+4:offset+7]]
            self.lock = False


if __name__ == '__main__':
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
    d_thread = dataThread(1, 'dataT', '127.0.0.1')
    d_thread.start()

    # new ax
    axis = new_axis([0, 0, 0])
    lines = []
    #frame for the camera/head, right controller, left controller
    for i in range(3):
        lines.append(ax.plot([o[0], o[0] + axis[0][0]], [o[1], o[1] + axis[0][1]], [o[2], o[2] + axis[0][2]], color='r')[0])
        lines.append(ax.plot([o[0], o[0] + axis[1][0]], [o[1], o[1] + axis[1][1]], [o[2], o[2] + axis[1][2]], color='g')[0])
        lines.append(ax.plot([o[0], o[0] + axis[2][0]], [o[1], o[1] + axis[2][1]], [o[2], o[2] + axis[2][2]], color='b')[0])

    point_ani = animation.FuncAnimation(fig, update, frames=np.array([0]), fargs=(d_thread, point, lines),
                                      interval=1, blit=False)

    plt.show()
    print 'done'
