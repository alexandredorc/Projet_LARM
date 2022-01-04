#!/usr/bin/python3
import math, rospy
from geometry_msgs.msg import Twist
import cv2
import numpy as np
from cv_bridge import CvBridge
from sensor_msgs.msg import Image


rospy.init_node('image_test', anonymous=True)

def souris(event, x, y, flags, param):
    global lo, hi, color, hsv_px
    if event == cv2.EVENT_MOUSEMOVE:
        # Conversion des trois couleurs RGB sous la souris en HSV
        global frame
        px = frame[y,x]
        px_array = np.uint8([[px]])
        hsv_px = cv2.cvtColor(px_array,cv2.COLOR_BGR2HSV)
    
    if event==cv2.EVENT_MBUTTONDBLCLK:
        global image
        color=image[y, x][0]

    if event==cv2.EVENT_LBUTTONDOWN:
        if color>5:
            color-=1

    if event==cv2.EVENT_RBUTTONDOWN:
        if color<250:
            color+=1
            
    lo[0]=color-5
    hi[0]=color+5

bridge = CvBridge()

def callback(data):
    global frame
    frame = bridge.imgmsg_to_cv2(data, "bgr8")
    
    global image
    image=cv2.blur(frame, (7, 7))

    mask=cv2.inRange(image, lo, hi)
    mask=cv2.erode(mask, None, iterations=4)
    mask=cv2.dilate(mask, None, iterations=4)
    image2=cv2.bitwise_and(image, frame, mask= mask)
    cv2.putText(frame, "Couleur: {:d}".format(color), (10, 30), cv2.FONT_HERSHEY_DUPLEX, 1, color_info, 1, cv2.LINE_AA)
    
    # Affichage des compdata(255, 255, 255), 1, cv2.LINE_AA)

    elements=cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    if len(elements) > 0:
        c=max(elements, key=cv2.contourArea)
        ((x, y), rayon)=cv2.minEnclosingCircle(c)
        if rayon>30:
            cv2.circle(image2, (int(x), int(y)), int(rayon), color_info, 2)
            cv2.circle(frame, (int(x), int(y)), 5, color_info, 10)
            cv2.line(frame, (int(x), int(y)), (int(x)+150, int(y)), color_info, 2)
            cv2.putText(frame, "Objet !!!", (int(x)+10, int(y) -10), cv2.FONT_HERSHEY_DUPLEX, 1, color_info, 1, cv2.LINE_AA)


    cv2.imshow('Camera', frame)
    cv2.imshow('image2', image2)
    cv2.imshow('Mask', mask)
    cv2.waitKey(3)


color=0

lo=np.array([color-5, 100, 50])
hi=np.array([color+5, 255,255])
color_info=(0, 0, 255)

cv2.namedWindow('Camera')
cv2.setMouseCallback('Camera', souris)
hsv_px = [0,0,0]



rospy.Subscriber("/camera/color/image_raw", Image, callback )
# spin() enter the program in a infinite loop
print("Start display.py")
rospy.spin()