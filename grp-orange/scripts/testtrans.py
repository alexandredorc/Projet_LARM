#!/usr/bin/python3
import math, rospy
from geometry_msgs.msg import Twist,PoseStamped
import cv2
import numpy as np
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
import tf




# # Initialize a global variable

rospy.init_node('test', anonymous=True)
tfListener = tf.TransformListener()


def callback(data):
    global tfListener
    goal =data
    print(goal)
    local_goal= tfListener.transformPose("/base_footprint", goal)
    print(local_goal)
    
    
   

# def callback2(data):
#     global tfListener,goal
#     local_goal= tfListener.transformPose("/base_footprint", goal)
#     print(local_goal)


rospy.Subscriber("/goal", PoseStamped, callback )
# rospy.Timer(rospy.Duration(0,1),callback2, oneshot=False)
rospy.spin()