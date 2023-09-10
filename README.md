# Subü Tetra Otonom Tasks
# 🚩 Contents

- [Getting Started](#Getting-Started)
  *  [Draw Equilateral Triangle](#draw-equilateral-triangle)
      * [Message Files](#message-files)
      * [Algorithm](#algorithm)
  *  [Laser Scanning](#laser-scanning)
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












