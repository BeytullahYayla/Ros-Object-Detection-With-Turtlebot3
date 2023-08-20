#!/usr/bin/env python3
import rospy
import math
from geometry_msgs.msg import Twist
from aisec.msg import Triangle
def move(distance):
    velocity_publisher = rospy.Publisher('/cmd_vel', Triangle, queue_size=10)
    vel_msg = Triangle()

    # İleri git
    vel_msg.linear.x = 0.2  # Örneğin, 0.2 m/s hızında ileri git
    vel_msg.linear.y = 0
    vel_msg.linear.z = 0

    t0 = rospy.Time.now().to_sec()
    current_distance = 0

    while current_distance < distance:
        velocity_publisher.publish(vel_msg)
        t1 = rospy.Time.now().to_sec()
        current_distance = 0.2 * (t1 - t0)

    # Dur
    vel_msg.linear.x = 0
    velocity_publisher.publish(vel_msg)

def turn_robot(angle,direction):
   
    velocity_publisher = rospy.Publisher('/cmd_vel', Triangle, queue_size=10)
    vel_msg = Triangle()

    # Dön
    if direction=="positive":
        
        vel_msg.angular.z = 0.5  # Örneğin, 0.5 rad/s hızında dön
    elif direction=="negative":
        vel_msg.angular.z=-0.5
        
    t0 = rospy.Time.now().to_sec()
    current_angle = 0

    while current_angle < angle:
        velocity_publisher.publish(vel_msg)
        t1 = rospy.Time.now().to_sec()
        current_angle = 0.5 * (t1 - t0)

    # Dur
    vel_msg.angular.z= 0
    velocity_publisher.publish(vel_msg)

rospy.init_node('robot_movement_node', anonymous=True)


try:
    
        
        
        move(1)  # 3 metre ileri git
        rospy.sleep(1)  # 1 saniye bekle
        turn_robot(math.radians(60),"negative")  # 120 derece dön (radyan cinsinden)
        rospy.sleep(1)  # 1 saniye bekle
        move(1)
        turn_robot(math.radians(120),"positive")  
        rospy.sleep(1)  # 1 saniye bekle
        move(1)
        rospy.sleep(1)  # 1 saniye bekle
        turn_robot(math.radians(120),"positive")
        rospy.sleep(1)  # 1 saniye bekle
        move(1)     
        rospy.sleep(1) 
        
        
except rospy.ROSInterruptException:
        print("Calisma Durdu")
