#!usr/bin/env python

import rospy
import math
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion


def callback(data):
    
    #from quaternion to euler
    orientation_q = data.pose.pose.orientation
    orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
    #we are interested in yaw since our robot can move only forward(x) or turn around(yaw)
    (roll, pitch, yaw) = euler_from_quaternion(orientation_list)

    #robots pose and orientation
    x = data.pose.pose.position.x
    y = data.pose.pose.position.y
    psi = yaw
    # rospy.loginfo("pose x is:%s", x)
    # rospy.loginfo("pose y is:%s", y)
    # rospy.loginfo("pose psi is:%s", yaw)

    #first robot stop
    x_goal = 2.0
    y_goal = 2.0
    psi_goal = 0.0
    #increasing the robots goals 2,2,0 --> 4,4,0 --> 6,6,0 --> 8,8,0 and prints a message when reaching goal
    if (x >= 1.998) and (y >= 1.998) and (psi_goal - psi < 0.01):
        if (x_goal == 2):
            x_goal = 4.0
            y_goal = 4.0
            rospy.loginfo_once("Reached goal 2,2,0")
    if (x >= 3.998) and (y >= 3.998) and (psi_goal - psi < 0.01):
        if (x_goal == 4.0):
            x_goal = 6.0
            y_goal = 6.0
            rospy.loginfo_once("Reached goal 4,4,0")
    if (x >= 5.998) and (y >= 5.998) and (psi_goal - psi < 0.01):
        if (x_goal == 6.0):
            x_goal = 8.0
            y_goal = 8.0
            rospy.loginfo_once("Reached goal 6,6,0")


    g = 0.3
    k = 0.5
    h = 0.8

    #calculations needed for u (linear) kai w (angular)
    e = math.sqrt(math.pow((x - x_goal), 2) + math.pow((y - y_goal), 2))
    theta = math.atan2(-(y-y_goal), -(x-x_goal))
    a = theta-psi

    # doing the calculations needed to move the robot and publish the message
    if (x < 7.998) and (y < 7.998):

        #preparing motion control data to return to cmd_vel
        u = (g * math.cos(a)) * e
        w = k * a + g * ((math.cos(a)*math.sin(a)) / a) * (a + (h*theta))

        #results in cmd_vel (linear.x and angular.z) 
        msg.linear.x = u
        msg.angular.z = w
        pub.publish(msg)  
    # this if statement is going to be used only when robot reached the goal 8,8,0 and shuts down the node
    elif (x > 7.999) and (y > 7.999) and (psi_goal - psi < 0.01):
        u = 0.0
        w = 0.0
        msg.linear.x = u
        msg.angular.z = w
        pub.publish(msg) 
        rospy.loginfo_once("Reached final goal 8,8,0")
        rospy.signal_shutdown("EOP")
  
  
if __name__ == '__main__':
    try:
        #creating node for motion control
        rospy.init_node('motion_control', anonymous=True)

        #publishing to cmd_vel
        pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        msg = Twist()

        #subscribing to odom for robots data of position and orientation
        rospy.Subscriber("/odom", Odometry, callback)
        #keeps the node running
        rospy.spin()
    except rospy.ROSInterruptException:
      pass
