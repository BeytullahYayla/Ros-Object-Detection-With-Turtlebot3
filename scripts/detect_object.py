#!/usr/bin/env python3
# -- coding: utf-8 --


import rospy
from find_object_2d.msg import ObjectsStamped
import cv2
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from aisec.msg import VisualData
class NesneTanima():
    def __init__(self):
        rospy.init_node("nesne_tanima")
        rospy.Subscriber("objectsStamped", ObjectsStamped, self.nesneTani)
        self.cv_bridge=CvBridge()
        rospy.Subscriber("camera/rgb/image_raw",VisualData,self.cameraCallback)
        rospy.spin()
    
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
        gray_image=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        _,threshold=cv2.threshold(gray_image,127,255,cv2.THRESH_BINARY)
        M=cv2.moments(threshold)
        x=int(M['m10']/M['m00'])
        y=int(M['m01']/M['m00'])
        print(x,y)
        
        cv2.circle(image,(x,y),5,(0,255,0),-1)
        cv2.imshow("image",image)
        cv2.imshow("gray_image",gray_image)
        cv2.waitKey(1)
        
                
    
        
        
        
NesneTanima()