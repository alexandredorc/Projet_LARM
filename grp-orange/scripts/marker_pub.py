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

def init_markers(x,y,z,id,time):
    marker = Marker()
    marker.header.frame_id = 'map' #self.global_frame
    marker.header.stamp=time
    marker.ns= "marker"
    marker.id= id
    marker.type = 1
    marker.action = 0
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
    marker.scale.x = 0.1
    marker.scale.y = 0.1
    marker.scale.z = 0.2
    return marker

def init_PoseStamped(x,y,time):
    Pose = PoseStamped()
    Pose.header.frame_id = 'camera_link'
    Pose.header.stamp= time
    Pose.pose.position.x= x
    Pose.pose.position.y= y
    Pose.pose.position.z= 0.0
    Pose.pose.orientation.x = 0.0
    Pose.pose.orientation.y = 0.0
    Pose.pose.orientation.z = 0.0
    Pose.pose.orientation.w = 1.0
    return Pose

def marker(x,y,z,id,time):
    bottle= init_markers(x,y,z,id,time)
    commandPublisher.publish(bottle)
def marker_delete(coor,id,time):
    delete_bottle=init_markers(coor[0],coor[1],0,id,time)
    delete_bottle.action=Marker.DELETE
    commandPublisher.publish(delete_bottle)
