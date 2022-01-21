#!/usr/bin/python3
import sys, math, rospy, rospkg
from geometry_msgs.msg import Twist, PoseStamped
import cv2
import numpy as np
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
import message_filters

sys.path.append( rospkg.RosPack().get_path('grp-orange') )

from scripts.marker_pub import *
import tf

#calcule des coordonées réel à partir de la profondeur et des coordonées sur l'image 
def realCoor(x,y,dist):
    angle=43.5*(x-640)/640
    angle=angle*math.pi/180
    return [math.cos(angle) * dist, math.sin( angle ) * dist-35]

#affiche les informations relatives à la detection de la bouteille
def display_info(rec,x,y,frame,image,mask):
    cv2.rectangle(frame, (int(rec[0]), int(rec[1])), (int(rec[0])+int(rec[2]), int(rec[3])+int(rec[1])), color_info, 2)
    cv2.circle(frame, (int(x), int(y)), 5, color_info, 10)
    cv2.line(frame, (int(x), int(y)), (int(x)+150, int(y)), color_info, 2)
    cv2.putText(frame, "Objet !!!", (int(x)+10, int(y) -10), cv2.FONT_HERSHEY_DUPLEX, 1, color_info, 1, cv2.LINE_AA)
            
#affiche le flux de la caméra, le masque et le resultat du masque sur le flux camera
def display_images(frame,image,mask):
    stencil=cv2.bitwise_and(image, frame, mask= mask)
    cv2.putText(frame, "Couleur: {0} {1} {2}".format(color[0],color[1],color[2]), (10, 30), cv2.FONT_HERSHEY_DUPLEX, 1, color_info, 1, cv2.LINE_AA)
    cv2.imshow('Camera', frame)
    #cv2.imshow('Stencil', stencil)
    cv2.imshow('Mask', mask)

    cv2.waitKey(3)

def image_proc(data):
    global depth_data
    timeStamp= data.header.stamp

    frame = bridge.imgmsg_to_cv2(data, "bgr8")

    #détection des couleurs orange
    image=cv2.blur(frame, (7, 7))
    mask=cv2.inRange(image, lo_or, hi_or)
    mask=cv2.erode(mask, None, iterations=6)
    mask=cv2.dilate(mask, None, iterations=6)
    
    elements=cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    close_elem=[]
    #garde les éléments de la même couleur que une bouteille qui ce trouve dans une zone précise 
    for e in elements:
        rec=cv2.boundingRect(e)
        x=int(rec[0]+(rec[2])/2)
        y=int(rec[1]+(rec[3])/2)
        depth_bottle=depth_data[y,x]
        bottle_shape=cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        if depth_bottle >= 150 and depth_bottle < 1500 and cv2.contourArea(e)>300:
            close_elem.append(bottle_shape)

    if len(close_elem) > 0 and depth_data is not None:
        
        x=int(rec[0]+(rec[2])/2)
        y=int(rec[1]+(rec[3])/2)

        depth_bottle=depth_data[y,x]
        coor= realCoor(x,y,depth_bottle)

        if  depth_bottle >= 150 and depth_bottle < 1500:
            #display_info(rec,x,y,frame,image,mask)
            gestionBottle(coor[0]/1000,-coor[1]/1000,timeStamp)   
    #display_images(frame,image,mask)

    rate.sleep()

#fonction permettant de gerer les marker en fonction des bouteilles qui sont détecter
def gestionBottle(x,y,time):
    global bottles
    createPose = init_PoseStamped(x,y,time)
    transfPose = tfListener.transformPose("map", createPose )

    x=transfPose.pose.position.x
    y=transfPose.pose.position.y

    #permet d'ajouter un marker s'il n'y a pas d'autre marker dans les environs
    if all(( math.sqrt((x-aBottle[0])**2 + (y-aBottle[1])**2))>0.3 for aBottle in bottles):
        bottles.append([x,y,1])
        
    else:
        #regarde toutes les bouteilles et regarde elle à déjà été indentifié
        for id,aBottle in enumerate(bottles):
            if math.sqrt((x-aBottle[0])**2 + (y-aBottle[1])**2) < 0.40 :
                x=(x+aBottle[0]*9)/10
                y=(y+aBottle[1]*9)/10
                bottles[id][0]=x
                bottles[id][1]=y
                bottles[id][2]+=1
                #affiche le marker si il à été vu 10 fois ou plus
                if bottles[id][2]>15:
                    marker(x,y,0,id+1,time)
                #permet de fusionner les bouteilles qui sont très proches
                for id2 in range(0,id,1):
                    dist= math.sqrt((bottles[id2][0]-aBottle[0])**2 + (bottles[id2][1]-aBottle[1])**2)
                 
                    if dist < 0.25 :
                        marker_delete(aBottle,id,time)
                        bottles.pop(id)   
     
#permet d'obtenir les données de profondeur
def get_depth(data):
    global depth_data
    depth_data = np.array(bridge.imgmsg_to_cv2(data, desired_encoding="passthrough"))

#fonction main
if __name__=="__main__":

    #print("(ง`_´)ง")#(0ง`_´)ง
    rospy.init_node('image_proc', anonymous=True)

    bridge = CvBridge()
    tfListener= tf.TransformListener()

    bottles=[]
    confirm_bottle=[]
    color=[15,80,230]
    color_info=(0, 0, 255)
    depth_data=None
    lo_or=np.array([0,130, 200])
    hi_or=np.array([50, 230,255])

    rospy.Subscriber("/camera/color/image_raw", Image, image_proc)
    rospy.Subscriber("/camera/aligned_depth_to_color/image_raw", Image , get_depth)

    rate=rospy.Rate(30) # spin() enter the program in a infinite loop
    rospy.spin()  