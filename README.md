# grp-orange repository for the UV LARM

https://ceri-num.gitbook.io/uv-larm/

This project aims to make the robot explore in autonomous his environment and detects bottles in it.

# Composition of the package

## scripts : We use 6 scripts. 3 of them start a node.
- [controler.py](#controler.py) : 
- [detection.py](#detection.py) :
- [main.py](#main.py) :
- [main_real.py](#main_real.py) :
- [marker_pub.py](#marker_pub.py) :
- [trace.py](#trace.py) :

## rviz 
- contains the rviz parameterized map

## launch 
- contains the launch that runs our whole project

# Explanation of the code

## challenge3_simulation.launch
In order to start all the nodes we need for a simulation, we make a launch.
This launch start :
- Gazebo with the map of the challenge 1 and a scan
- Our parametized RVIZ
- main.py, a script for autonomous movement
- trace.py, a script to follow the robot's path

## challenge3_turtlebot.launch
In order to start all the nodes we need to make the robot move and detect, we make this launch.
this launch start :
- the launch to connect the robot
- the scan
- the realsense camera
- the paramatized RVIZ
- main_real.py, a script for autonomous movement for the reality
- trace.py, a script to follow the robot's path

## detection.py 

In order to find the bottles on the screen, we decided to use the HSV method.

We have identified an HSV colour domain in which the colours on the orange bottles are found, we define an upper and lower bound which will create a mask from which we can identify shapes. 

```python
mask=cv2.inRange(image, lo_or, hi_or)
mask=cv2.erode(mask, None, iterations=6)
mask=cv2.dilate(mask, None, iterations=6)
elements=cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
```

Among all the shapes we will keep only the shapes that have a certain area and at a distance between 30cm and 1m50cm, the largest shape will give us the pixel position of our bottle. 

```python
if depth_bottle >= 150 and depth_bottle < 1500 and cv2.contourArea(e)>300:
```

Then we calculate via the coordinates of the bottle in the image and the depth at which the centre of the bottle is located. 

```python
width=43.5*sc_x/640
angle=43.5*(x-640)/640
angle=angle*math.pi/180
return [math.cos(angle) * dist, math.sin( angle ) * dist-35]
```

With this we can get the position of the bottle relative to the camera. We will apply a transform to the `/map` frame. 

```python
transfPose = tfListener.transformPose("map", createPose)
```

Once we have found the coordinates of the object, we check that it is not an object we already know by comparing their distance. If it is a new object, we add it to the list. If not, we modify its coordinates to adjust them. To avoid false detections, we only publish a marker in `/bottle` if the object has been seen at least 10 times.

## marker_pub.py 

this is a file that contains functions that allow us to manipulate the different markers in rviz. we can either add/modify or delete a marker. 


## controler.py

This file is creating the class Controler,

It has a `publisher` function that is transmiting the speed and spin data to the robot
```python
 def publisher(self): # cette fonction va transmettre les informations au robot
        cmd= Twist()
        if(self.speed>  self.speed_goal):
            self.speed-=0.02
        if(self.speed<  self.speed_goal):
            self.speed+=0.02
        cmd.angular.z= self.spin_goal
        cmd.linear.x= self.speed
        commandPublisher.publish(cmd)
```
It has a `check_path` function which enable the robot the have a special behaviour when it sees obscacles on both sides at a close distance. In that case it will calculate the distance between the two closest points on each sides.

***if the distance is greater than the robot size, then it will recognize the environment as a corridor:***
- speed: 0.25
- spin: 0

***if the distance is lower than the robot size; then it will recognize the environment as a corner:***
- speed: 0.03
- spin: ±1 (it will alternate between -1, 1)

## main.py

This file role is to decide how the robot linear and angular speed depending on the data given by the scanner. this file is config for the gazebo simulation.

the detection function is looking at the position of the closest object, we will then decide what are the spin and speed of the robot depending on the distance of the point, if the point is the closer then the spin will be greater and the speed lower.

## main_real.py

This file role is to decide how the robot linear and angular speed depending on the data given by the scanner. it is the same as the `main.py` file but adapt for the real kobuki robot.

## trace.py
This scripts subscribe to the odom topic and make markers in order to let appear the robot's path in RVIZ.

