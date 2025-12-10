# -*- coding: utf-8 -*-
#!/usr/bin/env python

import cv2
import numpy as np
import rospy
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image

class Detector:
    def __init__(self):
        self.bridge = CvBridge()
        self.cv_version = int(cv2.__version__.split('.')[0])

    def get_direction(self, message, line_color='red', tol=15):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(message, desired_encoding="bgr8")
        except CvBridgeError as e:
            rospy.logerr("CvBridge Error: {0}".format(e))
            return "none"

        h, w = cv_image.shape[:2]

        # Focus on bottom region of the image
        top = int(h * 0.75)
        bottom = int(h * 0.90)
        crop_img = cv_image[top:bottom, :]

        hsv = cv2.cvtColor(crop_img, cv2.COLOR_BGR2HSV)

        # Print HSV at center pixel (helpful for debugging)
        center_hsv = hsv[hsv.shape[0] // 2, hsv.shape[1] // 2]
        rospy.loginfo_throttle(1, "Center HSV: {}".format(center_hsv))

        # Define HSV thresholds for red
        lower_red1 = np.array([0, 100, 100])
        upper_red1 = np.array([10, 255, 255])
        lower_red2 = np.array([160, 100, 100])
        upper_red2 = np.array([180, 255, 255])

        # Create red mask
        mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
        mask = cv2.bitwise_or(mask1, mask2)

        # Morphological operations
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        # Check if any red is detected
        if np.count_nonzero(mask) == 0:
            rospy.logwarn_throttle(1, "Mask has no white pixels - red not detected")

        # Show red mask
        cv2.imshow("Red Mask", mask)

        debug_view = crop_img.copy()

        # Find contours
        if self.cv_version >= 4:
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        else:
            _, contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            largest = max(contours, key=cv2.contourArea)
            if cv2.contourArea(largest) > 300:
                x, y, w_box, h_box = cv2.boundingRect(largest)
                cv2.rectangle(debug_view, (x, y), (x + w_box, y + h_box), (0, 255, 0), 2)

                M = cv2.moments(largest)
                if M['m00'] > 0:
                    cx = int(M['m10'] / M['m00'])
                    center = debug_view.shape[1] // 2
                    offset = cx - center

                    cv2.line(debug_view, (center, 0), (center, debug_view.shape[0]), (255, 0, 0), 2)
                    cv2.circle(debug_view, (cx, y + h_box // 2), 5, (0, 0, 255), -1)

                    cv2.imshow("Debug View", debug_view)
                    cv2.waitKey(1)

                    if abs(offset) < tol:
                        return "center"
                    elif offset < 0:
                        return "left"
                    else:
                        return "right"
            else:
                rospy.logwarn_throttle(1, "Red contour too small to be valid")
        else:
            rospy.logwarn_throttle(1, "No red contour found")

        cv2.imshow("Debug View", debug_view)
        cv2.waitKey(1)
        return "none"
