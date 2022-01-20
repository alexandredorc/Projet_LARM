import math,rospy
from geometry_msgs.msg import Twist

class Controler: 
    def __init__(self):
        self.speed=0.2
        self.speed_goal=0.5
        self.spin_goal=0
        self.side=1
        self.corner=True

    def check_path(self, angle_min, dist_min): # cette fonction determine si le robot peut passer dans un chemin devant lui
        aPoint_G= [math.cos(angle_min[0]) * dist_min[0], math.sin( angle_min[0] ) * dist_min[0]]
        aPoint_D= [math.cos(angle_min[1]) * dist_min[1], math.sin( angle_min[1] ) * dist_min[1]]
        dist= math.sqrt((aPoint_G[0]-aPoint_D[0])**2+(aPoint_G[1]-aPoint_D[1])**2)
        if (dist<0.35):
            print("corner",self.side)
            self.corner=True
            self.spin_goal=self.side
            self.speed_goal=0.03
        else:
            self.speed_goal=0.25
            self.spin_goal=0

    def publisher(self): # cette fonction va transmettre les informations au robot
        cmd= Twist()
        if(self.speed>  self.speed_goal):
            self.speed-=0.02
        if(self.speed<  self.speed_goal):
            self.speed+=0.02
        
        cmd.angular.z= self.spin_goal
        cmd.linear.x= self.speed
        
        commandPublisher.publish(cmd)


commandPublisher = rospy.Publisher(
    '/cmd_vel_mux/input/navi',
    Twist, queue_size=10
)
