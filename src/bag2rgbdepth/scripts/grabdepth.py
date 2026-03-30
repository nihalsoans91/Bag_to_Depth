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
depth_mem = None
first_flag = True
output_folder = "."


def normalize_depth(image, max_val):
    """Scale a depth image to 0-255 for JPEG visualization."""
    if max_val == 0:
        return np.zeros_like(image, dtype=np.uint8)
    return (np.array(image, dtype=np.float32) * 255.0 / max_val).astype(np.uint8)


def checkdepth(msg):
    global i, depth_mem, first_flag
    try:
        cv_image = cvb.imgmsg_to_cv2(msg, msg.encoding)
    except CvBridgeError as e:
        rospy.logerr("cv_bridge error: %s", e)
        return

    numpy_image = np.array(cv_image, dtype=np.uint16)
    image_visual = normalize_depth(cv_image, np.max(cv_image))

    if first_flag:
        first_flag = False
        depth_mem = np.copy(numpy_image)
        _save_frame(i, numpy_image, image_visual)
        i += 1
        return

    if (depth_mem == numpy_image).all():
        return

    depth_mem = np.copy(numpy_image)
    _save_frame(i, numpy_image, image_visual)
    i += 1


def _save_frame(index, raw_array, visual_array):
    base = os.path.join(output_folder, "dframe{}".format(index))
    np.save(base + ".npy", raw_array)
    cv2.imwrite(base + ".jpg", visual_array)
    rospy.loginfo("Saved depth frame %d", index)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: grabdepth.py <output_folder>")
        sys.exit(1)

    output_folder = sys.argv[1]
    os.makedirs(output_folder, exist_ok=True)

    rospy.init_node("grabdepth")
    rospy.loginfo("Running Depth Grabber -> %s", output_folder)
    rospy.Subscriber("/camera/depth_registered/image_raw", Image, checkdepth)
    rospy.spin()
    rospy.loginfo("Depth Grabber done. Saved %d frames.", i)
