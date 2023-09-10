#! /usr/bin/env python3

import rospy
from aisec.msg import Triangle,Lidar,Robot

class Laser():
    def __init__(self) -> None:
        rospy.init_node("laser")#Start ros node
        rospy.Subscriber("scan",Lidar,callback=self.laserCallback)#Subscribe scan topic with custom Lidar message file
        self.pub=rospy.Publisher("cmd_vel",Triangle,queue_size=10)
        self.speed_message=Triangle()# Speed message as type custom Triangle message
        rospy.spin()
    
    def laserCallback(self,request):
        # If we think ranges values as circle we can scan specific area and get results with specified angles. Below, we get front,back,right and left values in order to check distance of obstacle in environemnt. 
        right_front=list(request.ranges[0:9])
        left_front=list(request.ranges[350:359])
        front=right_front+left_front
        left=list(request.ranges[80:100])
        right=list(request.ranges[260:280])
        back=list(request.ranges[170:190])
        min_left=min(left)
        min_right=min(right)
        min_back=min(back)
        min_front=min(front)
        print(min_left,min_right,min_front,min_back)
        
        if min_front>1.0:#If min front greater than 1 meter
             self.speed_message.linear.x=0.25#Than we can move on
             self.pub.publish(self.speed_message)#Publish speed message
        if min_front<1.0:
            self.speed_message.linear.x=0#Stop robot
            self.pub.publish(self.speed_message)#Publish speed message
    
        
            
        
Laser()