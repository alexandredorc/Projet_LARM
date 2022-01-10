import math, rospy
from geometry_msgs.msg import Twist
import cv2
import numpy as np
from visualization_msgs.msg import Marker
from geometry_msgs.msg import Pose

commandPublisher = rospy.Publisher(
    '/bottle',
    Marker, queue_size=10
)

def _init_markers(x,y,z):
    print("test")
    marker = Marker()
    marker.header.frame_id = 'camera_link' #self.global_frame
    marker.header.stamp=rospy.Time.now()
    marker.ns= "marker"
    #marker.id= 0
    marker.type = 1
    marker.action = Marker.ADD
    marker.pose.position.x= x
    marker.pose.position.y= y
    marker.pose.position.z= z
    marker.lifetime= rospy.Duration.from_sec(10)
    marker.pose.orientation.x = 0.0
    marker.pose.orientation.y = 0.0
    marker.pose.orientation.z = 0.0
    marker.pose.orientation.w = 1.0
    marker.color.r = 0.0
    marker.color.g = 1.0
    marker.color.b = 0.0
    marker.color.a = 1.0
    marker.scale.x = 1
    marker.scale.y = 1
    marker.scale.z = 1.0
    return marker

def marker_publish(x,y,z):
    bottle= _init_markers(x,y,z)
    commandPublisher.publish(bottle)


 



