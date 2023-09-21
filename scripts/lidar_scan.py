#! /usr/bin/env python3

import rospy
from aisec.msg import Triangle,Lidar,Robot

class Laser():
    def __init__(self) -> None:
        rospy.init_node("laser")
        rospy.Subscriber("scan",Lidar,callback=self.laserCallback)
        self.pub=rospy.Publisher("cmd_vel",Triangle,queue_size=10)
        self.speed_message=Triangle()
        rospy.spin()
    
    def laserCallback(self,request):
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
        
        if min_front>1.0:
             self.speed_message.linear.x=0.25
             self.pub.publish(self.speed_message)
        if min_front<1.0:
            self.speed_message.linear.x=0
            self.pub.publish(self.speed_message)
    
        
            
        
Laser()