#!/usr/bin/env python3
# -- coding: utf-8 --


import rospy
from find_object_2d.msg import ObjectsStamped
import cv2
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from aisec.msg import VisualData,Triangle,Lidar
import numpy as np
class NesneTanima():
    def __init__(self):
        rospy.init_node("nesne_tanima")#Initialize ros node
        self.pub=rospy.Publisher("cmd_vel",Triangle,queue_size=10)
        self.speed_message=Triangle()
        rospy.Subscriber("objectsStamped", ObjectsStamped, self.nesneTani)
        self.cv_bridge=CvBridge()
        rospy.Subscriber("camera/rgb/image_raw",VisualData,self.cameraCallback)
        rospy.Subscriber("scan",Lidar,callback=self.laserCallback)#Subscribe scan topic with custom Lidar message file
        rospy.spin()
        
    
        
        
        
    def filterColor(self,gray_image,lower_color,upper_color):
        mask=cv2.inRange(gray_image,lower_color,upper_color)
        return mask
    
    def findGeometryCenter(self,mask):
        M=cv2.moments(mask)
        x=int(M['m10']/M['m00'])
        y=int(M['m01']/M['m00'])
        return (x,y)
        
        
    def nesneTani(self, mesaj):
        try:
            self.nesne_id = mesaj.objects.data[0]
            print(mesaj.objects.data)
            print(self.nesne_id)
            if self.nesne_id == 1:
                print("Koni Bulundu")
                
        except IndexError:
            print("Herhangi bir nesne bulunamadi !!!")
    def cameraCallback(self,request):
        
        image=self.cv_bridge.imgmsg_to_cv2(request,"bgr8")
        gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        lower_gray=np.array([30],dtype="uint8")
        upper_gray=np.array([150],dtype="uint8")
        mask=self.filterColor(gray,lower_gray,upper_gray)
        
        h,w,c=image.shape
        M=cv2.moments(mask)
        
        if M['m00']>0:
            x,y=self.findGeometryCenter(mask)
            deviation=x-w/2
            
            self.speed_message.linear.x=0.25
            self.speed_message.angular.z=-deviation/100
            cv2.circle(image,(x,y),5,(255,0,0),-1)
            self.pub.publish(self.speed_message)    
        elif M['m00']==0 or M['m00']<0:
            self.speed_message.linear.x=0.0
            self.speed_message.linear.z=0.0
            self.pub.publish(self.speed_message)
        
        cv2.imshow("image",image)
        cv2.imshow("gray_image",mask)
     

        cv2.waitKey(1)
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
        
        
                
    
        
        
        
object_detection=NesneTanima()
