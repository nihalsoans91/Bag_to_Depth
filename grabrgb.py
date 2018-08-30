#/usr/bin/env python

import rospy
import numpy as np
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
cvb=CvBridge()
i=0

def grabrgb(msg):
    global i
    global video
    try:
        cv_image = cvb.imgmsg_to_cv2(msg,msg.encoding)
    except CvBridgeError as e:
        print(e)
    
    image_normal= np.array(cv_image,dtype=np.uint8)
    
    np.save("./frame"+str(i)+".npy",image_normal)
    rospy.loginfo("Image Saved"+str(i))
    i+=1
    
if __name__ == '__main__':
    
    rospy.init_node("grabrgb")
    
    rate=rospy.Rate(25)
    
    while not rospy.is_shutdown():
        
        rospy.Subscriber("/camera/rgb/image_raw",Image,grabrgb)
        rate.sleep()
        
    
    
    
