#pragma once

#include <ros/package.h>
#include <ros/ros.h>
#include <ros/console.h>
#include <image_transport/image_transport.h>
#include <sensor_msgs/image_encodings.h>
#include <opencv2/highgui/highgui.hpp>
#include <cv_bridge/cv_bridge.h>
#include <sys/stat.h>

void RGBCallback(const sensor_msgs::ImageConstPtr& msg);
void DepthCallback(const sensor_msgs::ImageConstPtr& msg);

extern bool firstRGB;
extern bool firstDepth;
extern uint64_t rgbImages;
extern uint64_t depthImages;
extern image_transport::CameraSubscriber subdepth;
extern image_transport::CameraSubscriber subrgb;
extern cv_bridge::CvImagePtr cv_ptr_rgb;
extern std::string filename_home;
