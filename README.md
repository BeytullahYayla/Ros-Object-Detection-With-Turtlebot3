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
      * [Messag Files](#message-files)
      * [Class Definition](#class-definition)


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



# Object Detection and Finding Geometry Center


In this task our aim is to find object's geometry center and move our robot towards detected object.


## Message Files

### VisualData.msg

```

std_msgs/Header header
uint32 height
uint32 width
string encoding
uint8 is_bigendian
uint32 step
uint8[] data

```

##  Class Definition

<ul>
  <li>
    <b>__init__:</b> This is the constructor method. It initializes the ROS node, sets up publishers and subscribers, and initializes some variables.

  </li>
  <li>
    <b>filterColor:</b> This method takes a grayscale image and filters it based on specified lower and upper color thresholds. It returns a binary mask highlighting the pixels within the specified color range.

  </li>
  <li>
    <b>findGeometryCenter:</b> This method takes a binary mask and calculates the centroid (x, y coordinates) of the detected object.

  </li>
  <li>
    <b>cameraCallback: </b>This method is a callback function for the RGB camera image. It converts the received image to grayscale, applies a color filter, and calculates the centroid of the detected object. Based on the object's position and distance, it adjusts the robot's speed and direction.
  </li>
  <li>
    <b>laserCallback:</b> This method is a callback function for the lidar data. It processes the lidar ranges to get information about obstacles in different directions. It updates the self.min_front variable, which seems to represent the minimum distance in front of the robot.

  </li>
</ul>

To filter object from scene first we need to convert image to gray format.
```
gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)# Convert image gray format in order to track color

```
For this task our object to track has gray color. So I defined lower and upper color values as follows:

```
lower_gray=np.array([30],dtype="uint8")
upper_gray=np.array([150],dtype="uint8")


```
 After that i get mask with filterColor custom method that i created, we need to find moment of object and x,y points of geometry center to draw circle.
 ```

 mask=self.filterColor(gray,lower_gray,upper_gray)#Get proper mask extracted from image with lower and upper color values
 h,w,c=image.shape
 M=cv2.moments(mask)# Find moments from acquired mask
 if M['m00']>0:# If there is a geometry center 
            x,y=self.findGeometryCenter(mask)# find x and y points of object in mask

```

Then if we detect object we need to move robot towards to the object.

```

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

```

 ![image](https://github.com/BeytullahYayla/Basic_Ros_Applications/assets/78471151/dce7eec8-f61f-442c-b3e2-e7ccfac0d641)
 
In this part we check deviation and distance from object in order to prevent collision. We would like to stop robot when 1 meter remained to object. If min_front greater than 1, then move robot, and turn robot using deviation. If min_front smaller than 1 then we arrive at the destination. We need to stop. Finally we need to draw circle to the geometry center.

```
 elif M['m00']==0 or M['m00']<0:#If there is no object in scene that we want to track
            self.speed_message.linear.x=0.0#Stop to the robot 
            self.speed_message.linear.z=0.0
            self.speed_message.angular.z=0.5#Turn left to the robot until find an object to track
            self.pub.publish(self.speed_message)
```

If there is no object, stop robot and start turn robot until find an object to track setting angular.z=0.5. With this even if object can't detected by our camera we are looking for object in our environment to prevent zero division error in ROS.

### Result

https://github.com/BeytullahYayla/Basic_Ros_Applications/assets/78471151/e23f3c2e-9745-4d4a-b7db-9ca31de3292d



















