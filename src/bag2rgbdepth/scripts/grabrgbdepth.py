#/usr/bin/env python

import rospy
import numpy as np
import cv2
import sys
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
cvb=CvBridge()
i_rgb=0
i_depth=0
rgb_mem=None
depth_mem=None
first_flag_depth=True
first_flag_rgb=True
depth_folder = ""
rgb_folder = ""

def imnormalize(xmax,image):
    """
    Normalize a list of sample image data in the range of 0 to 1
    : image:image data.
    : return: Numpy array of normalize data
    """
    xmin = 0
    a = 0
    b = 255
    
    return ((np.array(image,dtype=np.float32) - xmin) * (b - a)) / (xmax - xmin)

def grabrgb(msg):
    global i_rgb
    global rgb_mem
    global first_flag_rgb
    if i_rgb <= i_depth :
        try:
            cv_image = cvb.imgmsg_to_cv2(msg,"bgr8")
        except CvBridgeError as e:
            print(e)
        
        image_normal= np.array(cv_image)
        if first_flag_rgb == True :
            rgb_mem = np.copy(image_normal)
            np.save(rgb_folder+"/frame"+str(i_rgb)+".npy",image_normal)
            cv2.imwrite(rgb_folder+"/frame"+str(i_rgb)+".jpg", image_normal)
            first_flag_rgb=False
        elif np.array_equal(rgb_mem,image_normal) :
            return
        else :
            rgb_mem = np.copy(image_normal)
            np.save(rgb_folder+"/frame"+str(i_rgb)+".npy",image_normal)
            cv2.imwrite(rgb_folder+"/frame"+str(i_rgb)+".jpg", image_normal)
        i_rgb+=1

def checkdepth(msg):
    global i_depth
    global depth_mem
    global first_flag_depth
    try:
        cv_image = cvb.imgmsg_to_cv2(msg,msg.encoding)
    except CvBridgeError as e:
        print(e)
    
    image_normal= np.array(imnormalize(np.max(cv_image),cv_image),dtype=np.uint8)
    numpy_image= np.array(cv_image,dtype=np.uint16)
    if first_flag_depth == True:
        depth_mem = np.copy(numpy_image)
        np.save(depth_folder+"/dframe"+str(i_depth)+".npy",numpy_image)
        cv2.imwrite(depth_folder+"/dframe"+str(i_depth)+".jpg", image_normal)
        first_flag_depth=False
    if (depth_mem==numpy_image).all() :
        return
    else:
        depth_mem = np.copy(numpy_image)
        np.save(depth_folder+"/dframe"+str(i_depth)+".npy",numpy_image)
        cv2.imwrite(depth_folder+"/dframe"+str(i_depth)+".jpg", image_normal)
    i_depth+=1
    
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("usage: grabrgbdepth.py rgbfolder depthfolder")
        exit(0)
    rgb_folder = sys.argv[1]
    depth_folder = sys.argv[2]
    rospy.init_node("grabrgb")
    rospy.loginfo("Running RGB Grabber")
    rospy.Rate(0.1)
    rospy.Subscriber("/camera/rgb/image_raw",Image,grabrgb)
    rospy.Subscriber("/camera/depth_registered/image_raw",Image,checkdepth)
    rospy.spin()