#!/usr/bin/python3
import math, rospy
from geometry_msgs.msg import Twist
import cv2
import numpy as np
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
import message_filters
from test_marker import *

rospy.init_node('image_test', anonymous=True)

def souris(event, x, y, flags, param):
    global lo, hi, color, hsv_px
    sensi=np.array([50,100,50])

    if event == cv2.EVENT_MOUSEMOVE:
        # Conversion des trois couleurs RGB sous la souris en HSV
        global frame
        px = frame[y,x]
        px_array = np.uint8([[px]])
        hsv_px = cv2.cvtColor(px_array,cv2.COLOR_BGR2HSV)
    
    if event==cv2.EVENT_MBUTTONDBLCLK:
        global image
        color=image[y, x]

    min_color=sensi
    max_color=255-sensi
    
    lo=np.amax(np.vstack((np.array(color),min_color)),axis=0)-sensi
    hi=np.amin(np.vstack((np.array(color),max_color)),axis=0)+sensi

   
bridge = CvBridge()


def realCoor(x,y,sc_x,sc_y,D):
    
    width=43.5*sc_x/640
    angle=43.5*(x-640)/640
    dist=D
    angle=angle*math.pi/180
    return [math.cos(angle) * dist, math.sin( angle ) * dist-35]

def callback(data):
    
    global frame
    frame = bridge.imgmsg_to_cv2(data, "bgr8")
    
    global image
    image=cv2.blur(frame, (7, 7))

    global depth_data
    
    #480 848  240 424
    mask=cv2.inRange(image, lo, hi)
    mask=cv2.erode(mask, None, iterations=4)
    mask=cv2.dilate(mask, None, iterations=4)
    image2=cv2.bitwise_and(image, frame, mask= mask)
    cv2.putText(frame, "Couleur: {0} {1} {2}ts.registerCallback(callback)".format(color[0],color[1],color[2]), (10, 30), cv2.FONT_HERSHEY_DUPLEX, 1, color_info, 1, cv2.LINE_AA)
    
    # Affichage des compdata(255, 255, 255), 1, cv2.LINE_AA)

    elements=cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]


    if len(elements) > 0:
        c=max(elements, key=cv2.contourArea)
        rec=cv2.boundingRect(c)
        x=int(rec[0]+(rec[2])/2)
        y=int(rec[1]+(rec[3])/2)
        depth=depth_data[y][x]
        coor= realCoor(x,y,rec[2],rec[3],depth)
        print("depth",depth/10)
        print(coor)
        rayon=500
        if rayon>30 and depth != 0:
            cv2.rectangle(frame, (int(rec[0]), int(rec[1])), (int(rec[0])+int(rec[2]), int(rec[3])+int(rec[1])), color_info, 2)
            cv2.circle(frame, (int(x), int(y)), 5, color_info, 10)
            cv2.line(frame, (int(x), int(y)), (int(x)+150, int(y)), color_info, 2)
            cv2.putText(frame, "Objet !!!", (int(x)+10, int(y) -10), cv2.FONT_HERSHEY_DUPLEX, 1, color_info, 1, cv2.LINE_AA)
            marker_publish(coor[0]/100,-coor[1]/100,0.5)



    cv2.imshow('Camera', frame)
    cv2.imshow('image2', image2)
    cv2.imshow('Mask', mask)

    cv2.waitKey(3)

    rate.sleep()


def depth_CB(data):
    global depth_data
    depth_data = np.array(bridge.imgmsg_to_cv2(data, desired_encoding="passthrough"))

    
color=[25,25,25]
depth_data=np.array([])
lo=np.array(color)-10
hi=np.array(color)+10
color_info=(0, 0, 255)

cv2.namedWindow('Camera')
cv2.setMouseCallback('Camera', souris)
hsv_px = [0,0,0]

rate=rospy.Rate(10)

rospy.Subscriber("/camera/color/image_raw", Image, callback )

rospy.Subscriber("/camera/aligned_depth_to_color/image_raw", Image , depth_CB)


print("(ง`_´)ง")#(ง`_´)ง

# spin() enter the program in a infinite loop
rospy.spin() 