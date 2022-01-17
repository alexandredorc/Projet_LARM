#!/usr/bin/python3
import math, rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan



def check_path(data, angle_G, angle_D, dist_min_G, dist_min_D): # cette fonction determine si le robot peut passer dans un chemin devant lui
    aPoint_G= [math.cos(angle_G) * dist_min_G, math.sin( angle_G ) * dist_min_G]
    aPoint_D= [math.cos(angle_D) * dist_min_D, math.sin( angle_D ) * dist_min_D]
    dist= math.sqrt((aPoint_G[0]-aPoint_D[0])**2+(aPoint_G[1]-aPoint_D[1])**2)
    if (dist<0.45):
        spin=1
        speed=0.01
    else:
        speed=0.2
        spin=0
    return speed,spin


def findClosest(data): # trouve les coordonées polaires des objets les plus proches à droite et à gauche
    angle= data.angle_min
    angle_min_G=0
    angle_min_D=0
    dist_min_G=100
    dist_min_D=100
    for aDistance in data.ranges :
        if 0.1 < aDistance and aDistance < 5.0 and angle > -1.57 and angle < 1.57:
            if angle < 0:
                if dist_min_G > aDistance:
                    dist_min_G=aDistance
                    angle_min_G=angle
            else:
                if dist_min_D > aDistance:
                    dist_min_D=aDistance
                    angle_min_D=angle
            
        angle+= data.angle_increment
    return angle_min_G, angle_min_D, dist_min_G, dist_min_D

def publisher(spin,speed): # cette fonction va transmettre les informations au robot
      
    cmd= Twist()
    global speed_actu
    global spin_actu
    if(speed>  speed_actu):
        speed_actu+=0.01
    if(speed<  speed_actu):
        speed_actu-=0.01
    if(speed>  speed_actu):
        spin_actu+=0.01
    if(speed<  speed_actu):
        spin_actu-=0.01
    cmd.angular.z= spin
    cmd.linear.x= speed_actu
    commandPublisher.publish(cmd)

def callback(data):
    angle_min_G, angle_min_D, dist_min_G, dist_min_D = findClosest(data)

    if dist_min_G < dist_min_D:
        dist_min=dist_min_G
        angle_min=angle_min_G
    else:
        dist_min= dist_min_D
        angle_min=angle_min_D

    speed=1
    spin=0

    if dist_min < 0.6: #si le robot detecte un objet à moins de 0,6

        if dist_min < 0.4 : #selection de la vitesse en fonction de la distance de l'objet le plus proche
            speed= 0.01
        elif dist_min < 0.5 :
            speed= 0.2
        elif dist_min >= 0.5 :
            speed= 0.3

        if angle_min > 0: #selection de la rotation en fonction de la distance de l'objet le plus proche
            spin = -0.2
            if dist_min < 0.5: 
                spin= -0.5
        elif angle_min < 0:
            spin = 0.2
            if dist_min < 0.5:
                spin=1
        else:
            spin=0

        # cette fonction gere le chemin pour les coins et les couloires
        if dist_min_D > dist_min_G-0.1 and dist_min_D < dist_min_G+0.1 :
            speed,spin=check_path(data,angle_min_G,angle_min_D,dist_min_G,dist_min_D)

    else: #si le robot ne detecte pas d'objet a 0,6 alors il va tout droit
        spin = 0
        speed = 3
    
    publisher(spin,speed)


# Initiglobal alize ROS::node
rospy.init_node('move', anonymous=True)

commandPublisher = rospy.Publisher(
    '/cmd_vel_mux/input/navi',
    Twist, queue_size=10
)

spin_actu=0
speed_actu=0

rospy.Subscriber("/scan", LaserScan, callback )
# spin() enter the program in a infinite loop
print("Start move.py")
rospy.spin()