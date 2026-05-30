# MobileBot

<video controls src="WhatsApp Video 2026-05-30 at 8.39.07 AM.mp4" title="title">realWorld</video>

A ROS-based mobile robot project for camera-guided line following using OpenCV and TurtleBot3 simulation. The system detects a colored path from a camera feed and autonomously generates velocity commands to follow the line in a Gazebo environment.

---

## Overview

MobileBot is designed to demonstrate the integration of computer vision and robot motion control within the ROS ecosystem. The robot processes camera images in real time, detects a target path using OpenCV-based image processing techniques, and adjusts its movement accordingly.

Key capabilities include:

- Real-time camera image processing
- OpenCV-based line detection
- Autonomous steering and velocity control
- ROS topic communication
- Gazebo simulation support
- Debug visualization for detection results

---

## Features

- Subscribes to camera image topics
- Converts ROS image messages into OpenCV frames
- Detects a red line using HSV color thresholding
- Computes line position relative to the robot
- Generates motion commands through `/cmd_vel`
- Publishes annotated debug images
- Compatible with TurtleBot3 and Gazebo simulation environments

---

## System Workflow

1. Camera images are received from ROS topics.
2. The lower portion of each frame is extracted for analysis.
3. Images are converted from BGR to HSV color space.
4. Color thresholding isolates the target red path.
5. Contours are detected and analyzed.
6. The largest contour is selected as the path.
7. The contour center is compared with the image center.
8. Motion commands are generated.

| Line Position | Robot Action |
|--------------|-------------|
| Center | Move Forward |
| Left | Turn Left |
| Right | Turn Right |
| Not Detected | Stop |

---

## Repository Structure

```text
MobileBot/
├── CMakeLists.txt
├── package.xml
├── red_course.world
├── launch/
│   └── line_follower.launch
├── scripts/
│   ├── detector.py
│   ├── follower.py
│   ├── motion.py
│   └── red_line_detector.py
└── README.md
```

---

## Attribution

This project incorporates concepts, implementation ideas, and code adaptations from the following open-source project:

**jonmartinezdeaguirre/turtlebot3_line_follower**

The original project is distributed under the MIT License.

Portions of this work were adapted and extended for this project, including integration, modification, and customization for the MobileBot platform and simulation environment.

Original repository:

https://github.com/jonmartinezdeaguirre/turtlebot3_line_follower

The authors of the original project deserve full credit for their contribution to the foundational line-following implementation on which this project builds.

---

## License

This project contains work derived from an MIT-licensed repository.

When redistributing this project, the original MIT License and copyright notice from the upstream repository should be preserved in accordance with the terms of the MIT License.

Additional modifications, integrations, and project-specific enhancements have been developed for the MobileBot project.
