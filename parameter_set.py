#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
from mavros_msgs.srv import ParamSet
from mavros_msgs.msg import ParamValue

def set_param(param: str, value:float):
    """_summary_

    Args:
        param (str): paremeter name at PX4
        value (float): value of parameter
    """
    change_param = rospy.ServiceProxy('/mavros/param/set', ParamSet,persistent=True)
    rospy.wait_for_service('/mavros/param/set',timeout=0.1)
    
    myparam = ParamValue()
    myparam.real = value
    out = change_param(param, myparam) 




if __name__=="__main__":
    rospy.init_node('param_set', anonymous=True)
    
    set_params()
    