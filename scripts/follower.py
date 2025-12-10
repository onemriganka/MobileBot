#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Image
from motion import MotionPlanner
from detector import Detector

class Follower:
    def __init__(self):
        rospy.init_node('line_follower', anonymous=True)
        self.detector = Detector()
        self.motion_planner = MotionPlanner()

        #Use correct camera topic here
        #camera_topic = "/robot/front_rgbd_camera/rgb/image_raw"
        camera_topic = "/camera/rgb/image_raw"
        rospy.Subscriber(camera_topic, Image, self.camera_callback)

        self.rate = rospy.Rate(40)

    def run(self):
        while not rospy.is_shutdown():
            try:
                self.rate.sleep()
            except rospy.ROSInterruptException:
                pass

    def camera_callback(self, msg):
        direction = self.detector.get_direction(msg, line_color='red', tol=15)
        self.motion_planner.move(direction)

if __name__ == '__main__':
    follower = Follower()
    follower.run()
