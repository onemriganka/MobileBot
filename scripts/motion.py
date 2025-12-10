#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist

class MotionPlanner:
    def __init__(self):
        self.velocity = Twist()
        #self.publisher = rospy.Publisher('/robot/move_base/cmd_vel', Twist, queue_size=10)
        self.publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

    def move(self, direction):
        if direction == "center":
            self.velocity.linear.x = 0.2
            self.velocity.angular.z = 0.0
        elif direction == "left":
            self.velocity.linear.x = 0.075
            self.velocity.angular.z = 0.15
        elif direction == "right":
            self.velocity.linear.x = 0.075
            self.velocity.angular.z = -0.15
        elif direction == "none":
            self.velocity.linear.x = 0.0
            self.velocity.angular.z = 0.0
        else:
            rospy.logwarn("Unknown direction command: {}".format(direction))
            self.velocity.linear.x = 0.0
            self.velocity.angular.z = 0.0

        rospy.loginfo("Direction: {}, Linear: {}, Angular: {}".format(
            direction, self.velocity.linear.x, self.velocity.angular.z
        ))
        self.publisher.publish(self.velocity)
