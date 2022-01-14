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


def souris(event, x, y, flags, param):
    global lo, hi, color, hsv_px
    sensi=np.array([30,80,30])

    if event == cv2.EVENT_MOUSEMOVE:
        # Conversion des trois couleurs RGB sous la souris en HSV
        global frame
        px = frame[y-1,x-1]
        px_array = np.uint8([[px]])
        hsv_px = cv2.cvtColor(px_array,cv2.COLOR_BGR2HSV)
    
    if event==cv2.EVENT_MBUTTONDBLCLK:
        global image
        color=image[y, x]

    min_color=sensi
    max_color=255-sensi
    
    lo=np.amax(np.vstack((np.array(color),min_color)),axis=0)-sensi
    hi=np.amin(np.vstack((np.array(color),max_color)),axis=0)+sensi


def realCoor(x,y,sc_x,sc_y,D):
    width=43.5*sc_x/640
    angle=43.5*(x-640)/640
    dist=D
    angle=angle*math.pi/180
    return [math.cos(angle) * dist, math.sin( angle ) * dist-35]

def display_info(rec,x,y):
    cv2.rectangle(frame, (int(rec[0]), int(rec[1])), (int(rec[0])+int(rec[2]), int(rec[3])+int(rec[1])), color_info, 2)
    cv2.circle(frame, (int(x), int(y)), 5, color_info, 10)
    cv2.line(frame, (int(x), int(y)), (int(x)+150, int(y)), color_info, 2)
    cv2.putText(frame, "Objet !!!", (int(x)+10, int(y) -10), cv2.FONT_HERSHEY_DUPLEX, 1, color_info, 1, cv2.LINE_AA)
            

def display_images():
    stencil=cv2.bitwise_and(image, frame, mask= mask)
    cv2.putText(frame, "Couleur: {0} {1} {2}".format(color[0],color[1],color[2]), (10, 30), cv2.FONT_HERSHEY_DUPLEX, 1, color_info, 1, cv2.LINE_AA)
    cv2.imshow('Camera', frame)
    #cv2.imshow('Stencil', stencil)
    cv2.imshow('Mask', mask)

    cv2.waitKey(3)

def image_proc(data):
    
    global frame
    global image
    global mask
    global depth_data
    global timeStamp
    timeStamp= data.header.stamp

    frame = bridge.imgmsg_to_cv2(data, "bgr8")
    
    image=cv2.blur(frame, (7, 7))
    mask=cv2.inRange(image, lo_or, hi_or)
    mask=cv2.erode(mask, None, iterations=6)
    mask=cv2.dilate(mask, None, iterations=6)
    
    elements=cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    close_elem=[]
    for e in elements:
        
        rec=cv2.boundingRect(e)
        x=int(rec[0]+(rec[2])/2)
        y=int(rec[1]+(rec[3])/2)
        depth_bottle=depth_data[y,x]
        bottle_shape=cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        max(bottle_shape, key=cv2.contourArea)
        if depth_bottle >= 150 and depth_bottle < 1500 and cv2.contourArea(e)>300:
            close_elem.append(bottle_shape)

   
    if len(close_elem) > 0 and depth_data is not None:
        
        x=int(rec[0]+(rec[2])/2)
        y=int(rec[1]+(rec[3])/2)

        depth_bottle=depth_data[y,x]
        coor= realCoor(x,y,rec[2],rec[3],depth_bottle)

        if  depth_bottle >= 150 and depth_bottle < 1500:
            display_info(rec,x,y)
            gestionBottle(coor[0]/1000,-coor[1]/1000,timeStamp)
            
    display_images()

    rate.sleep()

def gestionBottle(x,y,time):
    global tfListener, bottles
    createPose = init_PoseStamped(x,y,time)
    transfPose = tfListener.transformPose("map", createPose )

    x=transfPose.pose.position.x
    y=transfPose.pose.position.y

    if all(( math.sqrt((x-aBottle[0])**2 + (y-aBottle[1])**2))>0.3 for aBottle in bottles):
        bottles.append([x,y,1])
        
    else:
        for id,aBottle in enumerate(bottles):
            if math.sqrt((x-aBottle[0])**2 + (y-aBottle[1])**2) < 0.60 :
                print(id,"modif")
                x=(x+aBottle[0]*7)/8
                y=(y+aBottle[1]*7)/8
                bottles[id][0]=x
                bottles[id][1]=y
                bottles[id][2]+=1
                print(bottles[id][2], id)
                if bottles[id][2]>10:
                    marker(x,y,0,id+1,time)
            for id2 in range(0,id,1):
                dist= math.sqrt((bottles[id2][0]-aBottle[0])**2 + (bottles[id2][1]-aBottle[1])**2)
                print(dist,id,id2)
                if dist < 0.25 :
                    print(id,id2)
                    marker_delete(aBottle,id,time)
                    bottles.pop(id)

        
     
       
    print("nombres de marker",len(bottles))

def get_depth(data):
    global depth_data
    depth_data = np.array(bridge.imgmsg_to_cv2(data, desired_encoding="passthrough"))

if __name__=="__main__":

    print("(ง`_´)ง")#(0ง`_´)ง

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
    lo_red=np.array([20,130, 200])
    hi_red=np.array([40, 210,255])

    cv2.namedWindow('Camera')
    cv2.setMouseCallback('Camera', souris)

    rospy.Subscriber("/camera/color/image_raw", Image, image_proc)
    rospy.Subscriber("/camera/aligned_depth_to_color/image_raw", Image , get_depth)

    rate=rospy.Rate(30) # spin() enter the program in a infinite loop
    rospy.spin()  