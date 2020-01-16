import numpy as np
from math import sin, cos

def rotation(roll, pitch, yaw):
    #x->roll
    #y->pitch
    #z->yaw
    rx = np.array([[1, 0, 0], [0, cos(roll), -sin(roll)], [0, sin(roll), cos(roll)]])
    ry = np.array([[cos(pitch), 0, sin(pitch)], [0, 1, 0], [-sin(pitch), 0, cos(pitch)]])
    rz = np.array([[cos(yaw), -sin(yaw), 0], [sin(yaw), cos(yaw), 0], [0, 0, 1]])
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
