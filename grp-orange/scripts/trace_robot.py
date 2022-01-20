#!/usr/bin/python3
import math, rospy
import cv2
import numpy as np

from visualization_msgs.msg import Marker
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Pose, PoseStamped,Twist,Pose
import marker_pub
from sensor_msgs.msg import Image
import tf

rospy.init_node('traceMove', anonymous=True)

def trace(data):
    global timeStamp, tfListener,id
    id=id+1
    Point = marker_pub.init_PoseStamped(data.pose.pose.position.x,data.pose.pose.position.y,rospy.Time())
    Point.header.frame_id="odom"
    transfPoint = tfListener.transformPose("map", Point )
    marker_pub.marker_Points(transfPoint.pose.position.x,transfPoint.pose.position.y,0,id)

id = 0
timeStamp = None
tfListener= tf.TransformListener()

rospy.Subscriber("/odom", Odometry, trace)

rospy.spin()