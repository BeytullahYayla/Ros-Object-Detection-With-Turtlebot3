#! /usr/bin/env python3

import rospy
from aisec.msg import Triangle



def triangle_move():
    rospy.init_node("triangle_move")
    pub=rospy.Publisher("cmd_vel",Triangle)
    speed_message=Triangle()#Type of speed message
    speed_message.Linear.x=0.5#Speed of the robot
    distance=5
    displacement=0#Displacement value of the robot
    t0=rospy.Time.now().to_sec()#Starting time as second types
    while displacement<distance:
        pub.publish(speed_message)
        t1=rospy.Time.now().to_sec()#Current time to check robot's displacement value
        displacement=(t1-t0)*speed_message.linear_x
    speed_message.Linear.x=0
    pub.publish(speed_message)
    
triangle_move()
