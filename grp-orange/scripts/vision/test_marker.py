import math, rospy
from geometry_msgs.msg import Twist
import cv2
import numpy as np
from visualization_msgs.msg import Marker
from geometry_msgs.msg import Pose, PoseStamped

commandPublisher = rospy.Publisher(
    '/bottle',
    Marker, queue_size=10
)

def _init_markers(x,y,z,id):
    print("test")
    marker = Marker()
    marker.header.frame_id = 'map' #self.global_frame
    marker.header.stamp=rospy.Time.now()
    marker.ns= "marker"
    marker.id= id
    marker.type = 1
    marker.action = Marker.ADD
    marker.pose.position.x= x
    marker.pose.position.y= y
    marker.pose.position.z= z
    marker.lifetime= rospy.Duration.from_sec(0)
    marker.pose.orientation.x = 0.0
    marker.pose.orientation.y = 0.0
    marker.pose.orientation.z = 0.0
    marker.pose.orientation.w = 1.0
    marker.color.r = 0.0
    marker.color.g = 1.0
    marker.color.b = 0.0
    marker.color.a = 1.0
    marker.scale.x = 0.2
    marker.scale.y = 0.2
    marker.scale.z = 0.4
    return marker

def init_PoseStamped(x,y):
    Pose = PoseStamped()
    Pose.header.frame_id = 'camera_link'
    # Pose.header.stamp.secs= 0
    Pose.pose.position.x= x
    Pose.pose.position.y= y
    Pose.pose.position.z= 0
    Pose.pose.orientation.x = 0.0
    Pose.pose.orientation.y = 0.0
    Pose.pose.orientation.z = 0.0
    Pose.pose.orientation.w = 1.0
    return Pose

def marker_add(x,y,z,id):
    bottle= _init_markers(x,y,z,id)
    commandPublisher.publish(bottle)
def marker_modify(x,y,z,id):
    bottle= _init_markers(x,y,z,id)
    bottle.action = Marker.MODIFY
    commandPublisher.publish(bottle)

 



