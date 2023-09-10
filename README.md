# Subü Tetra Otonom Tasks
# 🚩 Contents

- [Getting Started](#Getting-Started)
  *  [Draw Equilateral Triangle](#draw-equilateral-triangle)
      * [Message Files](#message-files)
      * [Algorithm](#algorithm)
  *  [Laser Scanning](#laser-scanning)
      * [Message Files](#message-files)
      * [Algorithm](#algorithm)

  *  [Object Detection and Finding Geometry Center](#object-detection)

  # Draw Equilateral Triangle

https://github.com/BeytullahYayla/Basic_Ros_Applications/assets/78471151/0dfb8827-335b-40d9-967c-42ba889661ce

### Message Files
I have used 2 different message type in order to achieve move robot instead of Twist() message.
### Vector3.msg
This message file contains speed values by x, y and z coordinates. The contents of tihs file as follows:

```
float64 x
float64 y
float64 z
```
### Triangle.msg
This message file contains type of speed values using Vector3.msg message file as linear and angular. The contents of tihs file as follows:

```
Vector3 linear
Vector3 angular
```

We are going to use custom Triangle message instead of Twist message in order to make publish with cmd_vel topic in our script.

### Algorithm
![330px-Regular_polygon_3_annotated svg](https://github.com/BeytullahYayla/Basic_Ros_Applications/assets/78471151/ac3ead49-b9d7-400d-a3b9-6316844a4b2b)

To equilateral triangle we need to know specifications of equilateral triangle.
<ul>
 <li>
  It has three sides of the same length
 </li>
 <li>
  An equilateral triangle is also a regular polygon with all angles measuring 60°.
 </li>
</ul>

In order to draw this triangle i have followed this steps:
<ul>
 <li><b>ROS Initialization:</b> Firstly, initialized a ROS (Robot Operating System) node using rospy.init_node(), and assign the node name as "equilateral_triangle_node.</li>
 <li><b>ROS Publisher Initialization:</b> Created a publisher (pub) using rospy.Publisher() to send messages to a ROS topic named /cmd_vel. This topic is used to control the robot's movement. The message type used is Triangle.
</li>
 <li><b>draw_equilateral_triangle Function:</b> This function performs the drawing of the equilateral triangle. It calls the move_distance function to move along each side of the triangle and the rotate function for the turning operation. Each side of the triangle has the same length.</li>
 <li><b>move_distance Function:</b> This function allows the robot to move forward a specified distance. It uses linear_speed to move forward. The forward motion is achieved by using a loop to cover the specified distance. It stops the robot when the movement is completed.
</li>
 <li><b>rotate Function:</b> This function is used to rotate the robot by a specified angle. In our situation specified angle must be 120. The rotation is done using angular_speed to cover the specified angle using a loop. It stops the robot when the rotation is completed.</li>
 <li><b>Main Function:</b> The main() function initializes the ROS node, starts the publisher, and initiates the equilateral triangle drawing by calling the draw_equilateral_triangle function.</li>
</ul>



# Laser Scanning

In laser scanning task our aim is to stop robot before crush to the obstacle. For this we need to create custom message file as type LaserScan under the sensor_msgs package. 

## Lidar.msg

This message file contains informations like angle_min, angle_max , scan_time and most importantly ranges values which we are going to use in this task. 

```
std_msgs/Header header
float32 angle_min
float32 angle_max
float32 angle_increment
float32 time_increment
float32 scan_time
float32 range_min
float32 range_max
float32[] ranges
float32[] intensities

```

In ranges list each element specifies the distance of the measurement at an angle.

```
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
```
In this piece of code we are getting range values in order to control distance from the obstacle using ranges values in Lidar message. We need to acquire front range value to check distance of obstacle from the robot. Let me draw right_front, left_front and other range values on image.


![Ranges](https://github.com/BeytullahYayla/Basic_Ros_Applications/assets/78471151/f0995694-f5f3-4cd9-a9b4-5ccbde15d3ea)

Here are the values that returns the distance values of each range value.

After that we check front distance because we would like to stop robot before crush to obstacle. If front value smaller than 1 then we will publish 0 speed value. Except this we want to move robot forward. 

```
        if min_front>1.0:
            self.speed_message.linear.x=0.25
            self.pub.publish(self.speed_message)
        else:
            self.speed_message.linear.x=0
            self.pub.publish(self.speed_message)
```
Let we analyze results of this study in gazebo simulation environment that i created.

### Result

https://github.com/BeytullahYayla/Basic_Ros_Applications/assets/78471151/006f638a-3454-4fe4-81bd-61d774552011












