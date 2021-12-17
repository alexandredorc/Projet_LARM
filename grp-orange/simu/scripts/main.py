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
def check_path(data, angle_G, angle_D, dist_min_G, dist_min_D): 
    print("test")
    aPoint_G= [math.cos(angle_G) * dist_min_G, math.sin( angle_G ) * dist_min_G]
    aPoint_D= [math.cos(angle_D) * dist_min_D, math.sin( angle_D ) * dist_min_D]
    dist= math.sqrt((aPoint_G[0]-aPoint_D[0])**2+(aPoint_G[1]-aPoint_D[1])**2)
    if (dist<0.4):
        spin=6
        speed=0.2
    else:
        speed=1
        spin=0
    print(speed,spin)
    return speed,spin



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



    if dist_min < 0.5:

        if dist_min < 0.3 :
            speed= 0.01
        elif dist_min < 0.4 :
            speed= 0.2
    
        if dist_min >= 0.4 :
            speed= 0.5

        if angle_min > 0:
            spin = -0.5
            if dist_min < 0.4: 
                spin= -2.5
        elif angle_min < 0:
            spin = 0.5
            if dist_min < 0.4:
                spin=2.5
        else:
            spin=0

        if dist_min_D > dist_min_G-0.05 and dist_min_D < dist_min_G+0.05 :
            print("in")
            speed,spin=check_path(data,angle_min_G,angle_min_D,dist_min_G,dist_min_D)
    else:
        spin = 0
        speed = 0.8
    print(speed,spin)        
    cmd= Twist()
    cmd.angular.z= spin
    cmd.linear.x= speed
    commandPublisher.publish(cmd)

rospy.Subscriber("/scan", LaserScan, callB )
# spin() enter the program in a infinite loop
print("Start move.py")
rospy.spin()