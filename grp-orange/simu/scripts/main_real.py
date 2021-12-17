#!/usr/bin/python3
import math, rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan


global spin
global speed

spin=0
speed=0.5
# Initiglobal alize ROS::node
rospy.init_node('move', anonymous=True)

commandPublisher = rospy.Publisher(
    '/cmd_vel_mux/input/navi',
    Twist, queue_size=10
)

# Publish velocity commandes:
def move_command(data):
    # Compute cmd_vel here and publish... (do not forget to reduce timer duration)
    pass


# call the move_command at a regular frequency:
rospy.Timer( rospy.Duration(0.1), move_command, oneshot=False )

def callB(data):
    obstacles= []
    angle= data.angle_min
    angle_min_G=0
    angle_min_D=0
    dist_min_G=100
    dist_min_D=100
    for aDistance in data.ranges :
        if 0.1 < aDistance and aDistance < 5.0 and angle > -1.571 and angle < 1.571:
            aPoint= [math.cos(angle) * aDistance, math.sin( angle ) * aDistance]
            obstacles.append( aPoint )
            if angle < 0:
                if dist_min_G > aDistance:
                    dist_min_G=aDistance
                    angle_min_G=angle
            else:
                if dist_min_D > aDistance:
                    dist_min_D=aDistance
                    angle_min_D=angle
            
        angle+= data.angle_increment
    
    if dist_min_G < dist_min_D:
        dist_min=dist_min_G
        angle_min=angle_min_G
    else:
        dist_min= dist_min_D
        angle_min=angle_min_D



    if dist_min < 2 :
        if dist_min < 0.25 :
            speed= 0.01
        elif dist_min < 0.3 :
            speed= 0.1
    
        if dist_min >= 0.3 :
            speed= 0.3

        if angle_min > 0:
            spin = -0.2
            if dist_min < 0.3:
                spin= -0.5
        elif angle_min < 0:
            spin = 0.2
            if dist_min < 0.3:
                spin=0.5
        else:
            spin=0
        print(dist_min_G,dist_min_D)
        if dist_min_D > dist_min_G-0.05 and dist_min_D < dist_min_G+0.05 :
            spin=1
            speed=0
            print("testestestestets")
    else:
        spin = 0
        speed = 0.8
            
    cmd= Twist()
    cmd.angular.z= spin
    cmd.linear.x= speed
    commandPublisher.publish(cmd)

rospy.Subscriber("/scan", LaserScan, callB )
# spin() enter the program in a infinite loop
print("Start move.py")
rospy.spin()