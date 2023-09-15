#!/usr/bin/env python3
import rospy
from aisec.msg import Triangle

import math

def move_distance(pub, linear_speed, distance):
    twist = Triangle()

    
    twist.linear.x= linear_speed
    current_distance = 0
    rate = rospy.Rate(10)  # 10 Hz
    t0=rospy.Time.now().to_sec()

    while current_distance < distance and not rospy.is_shutdown():
        pub.publish(twist)
        t1=rospy.Time.now().to_sec()
        rate.sleep()
        current_distance += linear_speed * 0.1  # Distance = Speed * Time

    # Stop the robot
    twist.linear.x = 0
    pub.publish(twist)

def rotate(pub, angular_speed, angle):
    twist = Triangle()
    twist.angular.z = angular_speed

    current_angle = 0
    rate = rospy.Rate(10)  # 10 Hz

    while current_angle < angle and not rospy.is_shutdown():
        pub.publish(twist)
        rate.sleep()
        current_angle += angular_speed * 0.1  # Angle = Speed * Time

    # Stop the robot
    twist.angular.z = 0
    pub.publish(twist)

def draw_equilateral_triangle(pub, side_length):
    linear_speed = 0.25  # Adjust as needed
    angular_speed = 0.7854  # Adjust as needed

    for _ in range(3):
        move_distance(pub, linear_speed, side_length)
        rotate(pub, angular_speed, math.radians(120))

def main():
    rospy.init_node('equilateral_triangle_node', anonymous=True)
    pub = rospy.Publisher('/cmd_vel', Triangle, queue_size=10)

    side_length = 1.04  # Adjust as needed

    draw_equilateral_triangle(pub, side_length)
  


try:
        main()
except rospy.ROSInterruptException:
        pass