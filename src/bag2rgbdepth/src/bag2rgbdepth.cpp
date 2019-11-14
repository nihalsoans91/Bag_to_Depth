# include <bag2rgbdepth.h>

void RGBCallback(const sensor_msgs::ImageConstPtr& msg){
    ROS_INFO("RGB");
}
void DepthCallback(const sensor_msgs::ImageConstPtr& msg){
    ROS_INFO("Depth");
}

int main(int argc, char** argv)
{
    ros::init(argc,argv,"bag2Depth");
    ros::NodeHandle nh;
    image_transport::ImageTransport it(nh);
    ROS_INFO("Running");
    it.subscribe("/camera/rgb/image_raw", 1, RGBCallback);
    // it.subscribeCamera("/camera/rgb/image_raw",1, boost::bind(&RGBCallback, _1));
    // it.subscribeCamera("/camera/depth_registered/image_raw",1, boost::bind(&DepthCallback, _1));
    ROS_INFO("Spinning");
    ros::spin();

    return 0;
}