#!/usr/bin/python3
import math, rospy
from geometry_msgs.msg import Twist,PoseStamped
import cv2
import numpy as np
from cv_bridge import CvBridge
from sensor_msgs.msg import Image


rospy.init_node('test', anonymous=True)

def callback(data):
    print(data)


rospy.Subscriber("/goal", PoseStamped, callback )

rospy.spin()