#!/usr/bin/env python3
# -- coding: utf-8 --


import rospy
import cv2
from cv_bridge import CvBridge
from aisec.msg import VisualData,Triangle,Lidar
import numpy as np
class NesneTanima():
    def __init__(self):
        rospy.init_node("nesne_tanima")#Initialize ros node
        self.pub=rospy.Publisher("cmd_vel",Triangle,queue_size=10)
        self.speed_message=Triangle()
        self.cv_bridge=CvBridge()
        rospy.Subscriber("camera/rgb/image_raw",VisualData,self.cameraCallback)
        rospy.Subscriber("scan",Lidar,callback=self.laserCallback)#Subscribe scan topic with custom Lidar message file
        self.min_front=0
        rospy.spin()
        
    
        
        
        
    def filterColor(self,gray_image,lower_color,upper_color):
        """This method provides us to filter specified color and returns mask

        Args:
            gray_image : converted image from bgr8 to gray image
            lower_color : lower color value of object that will be tracked 
            upper_color : upper color value of object that will be tracked

        Returns:
            mask: filtered object with certain color
        """
        mask=cv2.inRange(gray_image,lower_color,upper_color)
        return mask
    
    def findGeometryCenter(self,mask):
        """This method provides to find geometry center's x and y coordinates of given mask

        Args:
            mask : filtered object matrix with certain color

        Returns:
            (x,y): x and y coordinates of detected object's geometry center
        """
        M=cv2.moments(mask)
        x=int(M['m10']/M['m00'])
        y=int(M['m01']/M['m00'])
        return (x,y)
        
        

    def cameraCallback(self,request):
        """
        This callBack method works everytime that we subscribe camera/rgb/image_raw topic. We detect object and object's x and y points of geometry center.

        Args:
            request (VisualData): Includes request as type VisualData message.
        """
        
        image=self.cv_bridge.imgmsg_to_cv2(request,"bgr8")# First bridge image message to cv2
        gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)# Convert image gray format in order to track color
        lower_gray=np.array([30],dtype="uint8")
        upper_gray=np.array([150],dtype="uint8")
        mask=self.filterColor(gray,lower_gray,upper_gray)#Get proper mask extracted from image with lower and upper color values
        
        h,w,c=image.shape
        M=cv2.moments(mask)# Find moments from acquired mask
        
        if M['m00']>0:# If there is a geometry center 
            x,y=self.findGeometryCenter(mask)# find x and y points of object in mask
            deviation=x-w/2# We would like to center camera. So we need to find deviation and turn right/left robot.
            if self.min_front>1.0:# If distance from object greater than 1 meter 
                
                self.speed_message.linear.x=0.25
                self.speed_message.angular.z=-deviation/100#Taking into consideration to deviation, turn right/left robot 
                self.pub.publish(self.speed_message)# publish speed message
            elif self.min_front<1.0:# If front distance smaller than 1 
                self.speed_message.linear.x=0.0#Stop robot, we arrived at the destination
                self.speed_message.angular.z=0.0
                self.pub.publish(self.speed_message)
            cv2.circle(image,(x,y),5,(255,0,0),-1)#draw circle using x and y coordinates
                
        elif M['m00']==0 or M['m00']<0:#If there is no object in scene that we want to track
            self.speed_message.linear.x=0.0#Stop to the robot 
            self.speed_message.linear.z=0.0
            self.speed_message.angular.z=0.5#Turn left to the robot until find an object to track
            self.pub.publish(self.speed_message)
        
        cv2.imshow("image",image)
        cv2.imshow("gray_image",mask)
     

        cv2.waitKey(1)
    def laserCallback(self,request):
        """This method works everytime that we subscribe scan topic.

        Args:
            request (Lidar): Includes request as type Lidar message.
        """
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
        
        self.min_front=min(front)
        print(min_left,min_right,self.min_front,min_back)
        
        
        
        
                
    
        
        
        
object_detection=NesneTanima()
