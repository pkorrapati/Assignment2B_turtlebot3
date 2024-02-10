#!/usr/bin/env python3

import rospy

from math import pi, radians

from geometry_msgs.msg import Twist
from std_srvs.srv import Empty

# Remaps (-pi/2, pi/2) to (0, 2pi)
def remapAngle(angle):
    return round((angle + (2*pi)) % (2*pi), 4)


class TurtleBot:

    def __init__(self):
        # Creates a node 'turtlebot_circle_driver'. Using anonymous=True makes it unique.
        rospy.init_node('turtlebot_circle_driver', anonymous=True)

        # Reset turtlesim by calling the reset service
        # Not necessary when running from for launch files
        rospy.wait_for_service('/gazebo/reset_world')
        resetTurtle = rospy.ServiceProxy('/gazebo/reset_world', Empty)
        resetTurtle()

        # Publisher which will publish to the topic '/cmd_vel'.
        self.velocity_publisher = rospy.Publisher('/cmd_vel',
                                                  Twist, queue_size=3)

        self.rate = rospy.Rate(50)        

    # def update_pose(self, data):
    #     """Callback function which is called when a new message of type Pose is
    #     received by the subscriber."""
    #     self.pose = data
    #     self.pose.x = round(self.pose.x, 4)
    #     self.pose.y = round(self.pose.y, 4)

    #     remappedAngle = remapAngle(self.pose.theta)

    #     if self.blank:
    #         self.rotations = 0            
    #         self.lastOrientation = remappedAngle
    #         self.blank = False
        
    #     if remappedAngle >= radians(0) and self.lastOrientation > radians(357):
    #         self.rotations += 1 
        
    #     self.lastOrientation = remappedAngle

    def traverseCircle(self):
        """Move in a circle."""
        
        # Get the input from the user.        
        r = rospy.get_param('~r')
        w = rospy.get_param('~w')

        vel_msg = Twist()

        # while self.blank:
        #     pass

        # while ((self.rotations*2*pi) + remapAngle(self.pose.theta)) < 2*pi:
        #     rospy.loginfo((self.rotations*2*pi) + remapAngle(self.pose.theta))

        vel_msg.linear.x = 0
        vel_msg.linear.y = 0
        vel_msg.linear.z = 0

        # Angular velocity in the z-axis.
        vel_msg.angular.x = 0
        vel_msg.angular.y = 0
        vel_msg.angular.z = 0

        # Publishing our vel_msg
        self.velocity_publisher.publish(vel_msg)


        print("sent")

        # Publish at the desired rate.
        self.rate.sleep()

        while True:
            # Linear velocity in the x-axis.
            vel_msg.linear.x = w * r
            vel_msg.linear.y = 0
            vel_msg.linear.z = 0

            # Angular velocity in the z-axis.
            vel_msg.angular.x = 0
            vel_msg.angular.y = 0
            vel_msg.angular.z = w

            # Publishing our vel_msg
            self.velocity_publisher.publish(vel_msg)

            # Publish at the desired rate.
            self.rate.sleep()

        # Stop motion
        vel_msg.linear.x = 0
        vel_msg.linear.y = 0
        vel_msg.linear.z = 0
        vel_msg.angular.x = 0
        vel_msg.angular.y = 0
        vel_msg.angular.z = 0
        self.velocity_publisher.publish(vel_msg)

        # If we press control + C, the node will stop.
        # rospy.spin()

if __name__ == '__main__':
    try:
        x = TurtleBot()
        x.traverseCircle()
    except rospy.ROSInterruptException:
        pass
