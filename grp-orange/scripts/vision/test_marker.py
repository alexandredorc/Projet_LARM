import math, rospy
from geometry_msgs.msg import Twist
import cv2
import numpy as np
from visualization_msgs.msg import Marker
from geometry_msgs.msg import Pose


def _init_markers():
    print("test")
    marker = Marker()
    marker.header.frame_id = 'map' #self.global_frame
    marker.header.stamp=rospy.Time.now()
    marker.ns= "marker"
    marker.id= 0
    marker.type = 3
    marker.action = Marker.ADD
    marker.pose.position.x= 1
    marker.pose.position.y= 1
    marker.pose.position.z= 1
    marker.pose.orientation.x = 0.0
    marker.pose.orientation.y = 0.0
    marker.pose.orientation.z = 0.0
    marker.pose.orientation.w = 1.0
    marker.color.r = 1.0
    marker.color.g = 0.0
    marker.color.b = 0.0
    marker.color.a = 1.0
    marker.scale.x = 1
    marker.scale.y = 1
    marker.scale.z = 1.0
    return marker

def callBack(data):
    bottle= _init_markers()
    commandPublisher.publish(bottle)
    print(bottle)

rospy.init_node("test")
 
commandPublisher = rospy.Publisher(
    '/bottle',
    Marker, queue_size=10
)

rospy.Timer( rospy.Duration(1.0), callBack, oneshot=True )

rospy.spin()
