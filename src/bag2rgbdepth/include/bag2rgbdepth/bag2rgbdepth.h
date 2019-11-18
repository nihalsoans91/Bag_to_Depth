#include <ros/package.h>
#include <ros/ros.h>
#include <ros/console.h>
#include <image_transport/image_transport.h>
#include <opencv2/highgui/highgui.hpp>
#include <cv_bridge/cv_bridge.h>

void RGBCallback(const sensor_msgs::ImageConstPtr& msg);
void DepthCallback(const sensor_msgs::ImageConstPtr& msg);

bool firstRGB = false;
bool firstDepth = false;
uint64_t rgbImages = 0;
uint64_t depthImages = 0;
image_transport::CameraSubscriber subdepth;
image_transport::CameraSubscriber subrgb;
cv_bridge::CvImagePtr cv_ptr_rgb;
