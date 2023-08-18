#! /usr/bin/env python3

import rospy
from aisec.msg import Triangle

def moveTurtle():
    rospy.init_node("triangle_move")
    pub=rospy.Publisher("cmd_vel",Triangle)
    speed_message=Triangle()
    speed_message.linear_x=0.5
    distance=5
    displacement=0
    t0=rospy.Time.now().to_sec()#Start time
    while displacement<distance:
        pub.publish(speed_message)
        t1=rospy.Time.now().to_sec()
        displacement=(t1-t0)*speed_message.linear_x
    
    speed_message.linear_x=0
    pub.publish(speed_message)
    
moveTurtle()