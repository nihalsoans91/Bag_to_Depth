#!/usr/bin/env python3

import os
import sys
import rospy
import numpy as np
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

cvb = CvBridge()
i = 0
rgb_mem = None
first_flag = True
output_folder = "."


def grabrgb(msg):
    global i, rgb_mem, first_flag
    try:
        cv_image = cvb.imgmsg_to_cv2(msg, "bgr8")
    except CvBridgeError as e:
        rospy.logerr("cv_bridge error: %s", e)
        return

    image_array = np.array(cv_image)

    if first_flag:
        first_flag = False
        rgb_mem = np.copy(image_array)
        _save_frame(i, image_array)
        i += 1
        return

    if np.array_equal(rgb_mem, image_array):
        return

    rgb_mem = np.copy(image_array)
    _save_frame(i, image_array)
    i += 1


def _save_frame(index, image_array):
    base = os.path.join(output_folder, "frame{}".format(index))
    np.save(base + ".npy", image_array)
    cv2.imwrite(base + ".jpg", image_array)
    rospy.loginfo("Saved RGB frame %d", index)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: grabrgb.py <output_folder>")
        sys.exit(1)

    output_folder = sys.argv[1]
    os.makedirs(output_folder, exist_ok=True)

    rospy.init_node("grabrgb")
    rospy.loginfo("Running RGB Grabber -> %s", output_folder)
    rospy.Subscriber("/camera/rgb/image_raw", Image, grabrgb)
    rospy.spin()
    rospy.loginfo("RGB Grabber done. Saved %d frames.", i)
