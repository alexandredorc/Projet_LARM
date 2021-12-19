# grp-orange repository for the UV LARM

https://ceri-num.gitbook.io/uv-larm/

This project goal is to be able to control a turtle type of robot in gazebo and in hobuki robots in reality.

To make htis project work you will need the package mb6-tbot to be download. follow this website indication 

> https://bitbucket.org/imt-mobisyst/mb6-tbot/src/master/

after executing the roscore command in the terminal. You can execute 2 différent launch files that start the control program in either the gazebo simulation:

> roslaunch grp-orange challendge1_simulation.launch

if you want to start the robot controling program execute the following command

>roslaunch grp-orange challendge1_turtlebot.launch
