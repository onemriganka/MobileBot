# -*- coding: utf-8 -*-
#!/usr/bin/env python

import rospy
import cv2
import numpy as np

from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image

class RedLineDetector:
    def __init__(self):
        rospy.init_node('red_line_detector', anonymous=True)

        self.bridge = CvBridge()

        # Subscribe to the camera feed topic
        self.image_sub = rospy.Subscriber("/robot/front_rgbd_camera/rgb/image_raw", Image, self.image_callback)

        # Publisher for the debug image with bounding box
        self.image_pub = rospy.Publisher("/red_line/debug_image", Image, queue_size=1)

        rospy.loginfo("Red Line Detector Node Started")

    def image_callback(self, msg):
        try:
            frame = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        except CvBridgeError as e:
            rospy.logerr("CvBridge error: {}".format(e))
            return

        # Focus on the bottom part of the image
        height, width = frame.shape[:2]
        roi = frame[int(0.75 * height):height, :]

        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

        # Create red masks using two HSV ranges
        lower_red1 = np.array([0, 100, 100])
        upper_red1 = np.array([10, 255, 255])
        lower_red2 = np.array([160, 100, 100])
        upper_red2 = np.array([180, 255, 255])

        mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
        red_mask = cv2.bitwise_or(mask1, mask2)

        # Morphological operations to reduce noise
        red_mask = cv2.erode(red_mask, None, iterations=2)
        red_mask = cv2.dilate(red_mask, None, iterations=2)

        # Use OpenCV 3.x behavior: three return values for findContours
        _, contours, _ = cv2.findContours(red_mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            largest = max(contours, key=cv2.contourArea)
            if cv2.contourArea(largest) > 300:
                x, y, w_box, h_box = cv2.boundingRect(largest)
                cv2.rectangle(roi, (x, y), (x + w_box, y + h_box), (0, 255, 0), 2)
                rospy.loginfo_throttle(1, "Red line detected")
            else:
                rospy.logwarn_throttle(1, "Contour area too small")
        else:
            rospy.logwarn_throttle(1, "No red contour found")

        # Show the red mask for debugging (optional)
        cv2.imshow("Red Mask", red_mask)
        cv2.imshow("ROI Debug", roi)
        cv2.waitKey(1)

        # Publish the annotated image
        try:
            debug_image_msg = self.bridge.cv2_to_imgmsg(roi, "bgr8")
            self.image_pub.publish(debug_image_msg)
        except CvBridgeError as e:
            rospy.logerr("CvBridge Error during publishing: {}".format(e))

if __name__ == '__main__':
    try:
        RedLineDetector()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
