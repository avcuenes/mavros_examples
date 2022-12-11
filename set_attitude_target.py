#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
from mavros_msgs.msg import AttitudeTarget
from geometry_msgs.msg import Quaternion, Vector3,TwistStamped
from mavros_msgs.srv import *
from std_msgs.msg import Header
from tf.transformations import quaternion_from_euler

def set_desired_attitude(desired_roll:float ,desired_pitch:float):
    """_summary_

    Args:
        desired_roll (float): _description_ roll angle in radian
        desired_pitch (float): _description_ pitch angle in radian
    """
    
    rospy.set_param('/mavros/setpoint_attitude/use_quaternion', True)
    
    att = AttitudeTarget()
    att_setpoint_pub = rospy.Publisher('mavros/setpoint_raw/attitude', AttitudeTarget, queue_size=1)

    rate = rospy.Rate(10)  # Hz
    att.body_rate = Vector3()
    att.header = Header()
    att.header.frame_id = "map"
    
    print("desired angle >>>>>> ",desired_roll*180/3.14)
    print("desired pitch >>>>>> ",desired_pitch*180/3.14)
    
    att.orientation = Quaternion(*quaternion_from_euler(desired_roll, desired_pitch,
                                                                0))
    att.thrust = 0.7
    att.type_mask = 7  # ignore body rate

    att.header.stamp = rospy.Time.now()
    att_setpoint_pub.publish(att)
    
    setOfboardMode()
    

def setOfboardMode():
    rospy.wait_for_service('/mavros/set_mode')
    flightModeService = rospy.ServiceProxy('/mavros/set_mode', mavros_msgs.srv.SetMode)
    #http://wiki.ros.org/mavros/CustomModes for custom modes
    isModeChanged = flightModeService(custom_mode='OFFBOARD') #return true or false
    
    
if __name__ == "__main__":
    
    rospy.init_node('set_desired_attitude', anonymous=True)
    
    set_desired_attitude(0.1,0.1)