#/usr/bin/env python

import rospy
import numpy as np
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
cvb=CvBridge()
i=0
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

def checkdepth(msg):
    global i
    global video
    try:
        cv_image = cvb.imgmsg_to_cv2(msg,msg.encoding)
    except CvBridgeError as e:
        print(e)
    
    image_normal= np.array(imnormalize(np.max(cv_image),cv_image),dtype=np.uint8)
    np.save("./frame"+str(i)+".npy",image_normal)
    rospy.loginfo("Image Saved"+str(i))
    i+=1
    
if __name__ == '__main__':
    
    rospy.init_node("depthtest")
    
    rate=rospy.Rate(25) #25hz
    
    while not rospy.is_shutdown():
        rospy.Subscriber("/camera/depth_registered/image_raw",Image,checkdepth)
    
        rate.sleep()
    
    
