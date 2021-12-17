#!/usr/bin/python3
import math, rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

# Initialize ROS::node
rospy.init_node('move', anonymous=True)

commandPublisher = rospy.Publisher(
    '/cmd_vel',
    Twist, queue_size=10
)

# Publish velocity commandes:
def move_command(data):
    # Compute cmd_vel here and publish... (do not forget to reduce timer duration)
    cmd= Twist()
    cmd.linear.x= 1
    commandPublisher.publish(cmd)

# call the move_command at a regular frequency:
rospy.Timer( rospy.Duration(0.1), move_command, oneshot=False )

def callB(data):
    obstacles= []
    angle= data.angle_min
    for aDistance in data.ranges :
        if 0.1 < aDistance and aDistance < 5.0 :
            aPoint= [math.cos(angle) * aDistance, math.sin( angle ) * aDistance]
            obstacles.append( aPoint )
        angle+= data.angle_increment
    """rospy.loginfo( str(
        [ [ round(p[0], 2), round(p[1], 2) ] for p in  obstacles[0:10] ] 
    ) + " ..." )"""
    dist_min=100
    angle_min=0
    for aDistance in data.ranges :
        if 0.1 < aDistance and aDistance < 0.5 :
            if dist_min > angle:
                dist_min=aDistance
                angle_min=angle
        angle+= data.angle_increment
    speed=0.5
    if angle_min > 0:
        spin= -1
    if angle_min < 0:
        spin= 1
    cmd= Twist()
    cmd.angular.z= spin
    cmd.linear.x= speed
    commandPublisher.publish(cmd)


rospy.Subscriber("/base_scan", LaserScan, callB )
# spin() enter the program in a infinite loop
print("Start move.py")
rospy.spin()