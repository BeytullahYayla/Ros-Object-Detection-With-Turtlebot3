#!/usr/bin/env python3

import rospy
from find_object_2d.msg import ObjectsStamped

class NesneTanima():
    def _init_(self):
        rospy.init_node("nesne_tanima")
        rospy.Subscriber("objectsStamped",ObjectsStamped,self.nesneTani)
        rospy.spin()
    
    def nesneTani(self,mesaj):
        try:
            self.nesne_id = mesaj.objects.data[0]
            print(self.nesne_id)
            if self.nesne_id == 1:
                print("Koni Bulundu")
        except IndexError:
            print("Herhangi bir nesne bulunamadi !!!")
        
NesneTanima()