#!/usr/bin/env python3

import os
import sys
import rospy
import numpy as np
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

cvb = CvBridge()
i_rgb = 0
i_depth = 0
rgb_mem = None
depth_mem = None
first_flag_depth = True
first_flag_rgb = True
depth_folder = ""
rgb_folder = ""


def normalize_depth(image, max_val):
    """Scale a depth image to 0-255 for JPEG visualization."""
    if max_val == 0:
        return np.zeros_like(image, dtype=np.uint8)
    return (np.array(image, dtype=np.float32) * 255.0 / max_val).astype(np.uint8)


def grabrgb(msg):
    global i_rgb, rgb_mem, first_flag_rgb
    if i_rgb > i_depth:
        return
    try:
        cv_image = cvb.imgmsg_to_cv2(msg, "bgr8")
    except CvBridgeError as e:
        rospy.logerr("cv_bridge RGB error: %s", e)
        return

    image_array = np.array(cv_image)

    if first_flag_rgb:
        first_flag_rgb = False
        rgb_mem = np.copy(image_array)
        _save_rgb(i_rgb, image_array)
        i_rgb += 1
        return

    if np.array_equal(rgb_mem, image_array):
        return

    rgb_mem = np.copy(image_array)
    _save_rgb(i_rgb, image_array)
    i_rgb += 1


def checkdepth(msg):
    global i_depth, depth_mem, first_flag_depth
    try:
        cv_image = cvb.imgmsg_to_cv2(msg, msg.encoding)
    except CvBridgeError as e:
        rospy.logerr("cv_bridge depth error: %s", e)
        return

    numpy_image = np.array(cv_image, dtype=np.uint16)
    image_visual = normalize_depth(cv_image, np.max(cv_image))

    if first_flag_depth:
        first_flag_depth = False
        depth_mem = np.copy(numpy_image)
        _save_depth(i_depth, numpy_image, image_visual)
        i_depth += 1
        return

    if (depth_mem == numpy_image).all():
        return

    depth_mem = np.copy(numpy_image)
    _save_depth(i_depth, numpy_image, image_visual)
    i_depth += 1


def _save_rgb(index, image_array):
    base = os.path.join(rgb_folder, "frame{}".format(index))
    np.save(base + ".npy", image_array)
    cv2.imwrite(base + ".jpg", image_array)
    rospy.loginfo("Saved RGB frame %d", index)


def _save_depth(index, raw_array, visual_array):
    base = os.path.join(depth_folder, "dframe{}".format(index))
    np.save(base + ".npy", raw_array)
    cv2.imwrite(base + ".jpg", visual_array)
    rospy.loginfo("Saved depth frame %d", index)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: grabrgbdepth.py <rgb_folder> <depth_folder>")
        sys.exit(1)

    rgb_folder = sys.argv[1]
    depth_folder = sys.argv[2]
    os.makedirs(rgb_folder, exist_ok=True)
    os.makedirs(depth_folder, exist_ok=True)

    rospy.init_node("grabrgbdepth")
    rospy.loginfo("Running RGB+Depth Grabber: rgb=%s depth=%s", rgb_folder, depth_folder)
    rospy.Subscriber("/camera/rgb/image_raw", Image, grabrgb)
    rospy.Subscriber("/camera/depth_registered/image_raw", Image, checkdepth)
    rospy.spin()
    rospy.loginfo("Done. Saved %d RGB frames, %d depth frames.", i_rgb, i_depth)
