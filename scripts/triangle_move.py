#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
import math

def draw_equilateral_triangle():
    rospy.init_node("draw_triangle_node")
    pub = rospy.Publisher("cmd_vel", Twist, queue_size=10)
    rate = rospy.Rate(10)  # Hz

    forward_distance = 5.0  # Eşkenar üçgenin bir kenarının uzunluğu (örneğin 1 metre)
    turn_angle = math.radians(60)  # Dönüş açısı (eşkenar üçgenin iç açısı) (örneğin 60 derece)
    num_sides = 3  # Üçgenin toplam kenar sayısı

    for _ in range(num_sides):
        # İleriye git
        cmd_vel_msg = Twist()
        cmd_vel_msg.linear.x = 0.5  # Örneğin, 0.2 m/s ilerleme hızı
        cmd_vel_msg.angular.z = 0.0
        pub.publish(cmd_vel_msg)
        rospy.sleep(forward_distance / cmd_vel_msg.linear.x)

        # Dön
        cmd_vel_msg.linear.x = 0.0
        cmd_vel_msg.angular.z = 0.5  # Örneğin, 0.2 rad/s dönme hızı
        pub.publish(cmd_vel_msg)
        rospy.sleep(turn_angle / cmd_vel_msg.angular.z)

    # Durdur
    cmd_vel_msg.linear.x = 0.0
    cmd_vel_msg.angular.z = 0.0
    pub.publish(cmd_vel_msg)

draw_equilateral_triangle()
