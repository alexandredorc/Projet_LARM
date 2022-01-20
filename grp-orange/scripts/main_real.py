#!/usr/bin/python3
import sys, rospy, rospkg
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan



sys.path.append( rospkg.RosPack().get_path('grp-orange') )
from scripts.controler import *


def findClosest(data): # trouve les coordonées polaires des objets les plus proches à droite et à gauche
    angle= data.angle_min
    angle_min=[0,0]
    dist_min=[100,100]
    for aDistance in data.ranges :
        if 0.1 < aDistance and aDistance < 5.0 and angle > -1.57 and angle < 1.57:
            side=0 if (angle < 0) else 1
            if dist_min[side]> aDistance:
                dist_min[side]=aDistance
                angle_min[side]=angle
        angle+= data.angle_increment
    return angle_min,dist_min

def callback(data):
    arr_angle_min, arr_dist_min = findClosest(data)
    dist_min=min(arr_dist_min)
    index=arr_dist_min.index(dist_min)
    angle_min=arr_angle_min[index]
    speed=0.3
    spin=0
    print("test")
    if dist_min < 0.7: #si le robot detecte un objet à moins de 0,6
        print("test 06")
        if dist_min < 0.5 : #selection de la vitesse en fonction de la distance de l'objet le plus proche
            speed= 0.01
            spin=1
        elif dist_min < 0.6 :
            speed= 0.2
        elif dist_min >= 0.6 :
            speed= 0.3

        if angle_min > 0: #selection de la rotation en fonction de la distance de l'objet le plus proche
            spin = -0.2
            if dist_min < 0.6: 
                spin= -0.5
        elif angle_min < 0:
            spin = 0.2
            if dist_min < 0.6:
                spin=0.5
        else:
            spin=0
        print(speed,spin)
        Tbot.spin_goal=spin
        Tbot.speed_goal=speed
        # cette fonction gere le chemin pour les coins et les couloires
        if arr_dist_min[0] > arr_dist_min[1]-0.1 and arr_dist_min[0] < arr_dist_min[1]+0.1 and dist_min < 0.5:
            Tbot.check_path(arr_angle_min,arr_dist_min)

    else: #si le robot ne detecte pas d'objet a 0,6 alors il va tout droit
        spin = 0
        speed = 0.5
        Tbot.spin_goal=spin
        Tbot.speed_goal=speed

    Tbot.publisher()


Tbot=Controler()

commandPublisher = rospy.Publisher(
    '/cmd_vel_mux/input/navi',
    Twist, queue_size=10
)

# Initialize  ROS::node
rospy.init_node('move', anonymous=True)


rospy.Subscriber("/scan", LaserScan, callback )
# spin() enter the program in a infinite loop
print("Start move.py")
rospy.spin()