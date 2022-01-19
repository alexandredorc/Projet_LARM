#!/usr/bin/python3
from asyncio.windows_events import NULL
import math, rospy
from sqlite3 import Timestamp
from turtle import tracer
import cv2
import numpy as np
from visualization_msgs.msg import Marker
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Pose, PoseStamped,Twist,Pose
import marker_pub
import tf

rospy.init_node('traceMove', anonymous=True)

def trace(data):
    global timeStamp, tfListener
    timeStamp = data.header.stamp
    Point = marker_pub.init_PoseStamped(data.pose.pose.position.x,data.pose.pose.position.y,timeStamp)
    transfPoint = tfListener.transformPose("map", Point )
    marker_pub.marker_Points(transfPoint.pose.position.x,transfPoint.pose.position.y,0,transfPoint.header.stamp)

timeStamp = None
tfListener= tf.TransformListener()

rospy.Subscriber("/odom", Odometry, trace)
rospy.spin()