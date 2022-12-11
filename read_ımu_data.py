#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
import numpy as np
from sensor_msgs.msg import Imu


def get_attitude():

    rospy.Subscriber("/mavros/imu/data", Imu, state_callback)
    rospy.wait_for_message("/mavros/imu/data", Imu)


def state_callback(data):
    roll,pitch,yaw = quaternion_to_euler_angle(data.orientation.x, data.orientation.y, data.orientation.z,data.orientation.w)
    rospy.loginfo("I heard %s",data.data)


def quaternion_to_euler_angle(x, y, z,w):
    qr = y * y

    t0 = +2.0 * (w * x + y * z)
    t1 = +1.0 - 2.0 * (x * x + qr)
    roll = np.degrees(np.arctan2(t0, t1))

    t2 = +2.0 * (w * y - z * x)
    t2 = np.clip(t2, a_min=-1.0, a_max=1.0)
    pitch = np.degrees(np.arcsin(t2))

    t3 = +2.0 * (w * z + x * y)
    t4 = +1.0 - 2.0 * (qr + z * z)
    yaw = np.degrees(np.arctan2(t3, t4))

    return roll,pitch,yaw 

if __name__ == "__main__":
    
    rospy.init_node('get_attitude', anonymous=True)
    
    get_attitude()