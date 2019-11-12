import numpy as np
from math import sin, cos

def rotation(roll, pitch, yaw):
    #x->pitch
    #y->yaw
    #z->roll
    rx = np.array([[1, 0, 0], [0, cos(pitch), -sin(pitch)], [0, sin(pitch), cos(pitch)]])
    ry = np.array([[cos(yaw), 0, sin(yaw)], [0, 1, 0], [-sin(yaw), 0, cos(yaw)]])
    rz = np.array([[cos(roll), -sin(roll), 0], [sin(roll), cos(roll), 0], [0, 0, 1]])
    rotation = np.dot(rz, ry)
    rotation = np.dot(rotation, rx)
    return rotation

def new_axis(angle):
    #input angle: roll, pitch, yaw
    rot = rotation(angle[0], angle[1], angle[2])
    new_vec = []
    new_vec.append(np.dot(rot, np.array([1, 0, 0])))
    new_vec.append(np.dot(rot, np.array([0, 1, 0])))
    new_vec.append(np.dot(rot, np.array([0, 0, 1])))
    return new_vec
