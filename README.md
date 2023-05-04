# ROS-turtlebot3-motion-control
ROS python script moving the robot from points 0,0,0 to 2,2,0 to 4,4,0 to 6,6,0 and lastly 8,8,0 using a unicycle robot control which is shown down below.

[Autonomous_Robotic_Vehicles_CS_UTH_Motion_Control.pdf](https://github.com/lUnderFinnedl/ROS-turtlebot3-motion-control/files/11400271/Autonomous_Robotic_Vehicles_CS_UTH_Motion_Control.pdf)


This node is subscribing to /odom and publishing to /cmd_vel of the robot doing all the needed calculations for the robot to move and stop on the desired marks

To run the node simply clone the file in turtlebot3_gazebo and run in terminal  
        python turtlebot3_motion_controller.py

This was an assignment for Programming Robotic Systems class of University of Thessaly.
