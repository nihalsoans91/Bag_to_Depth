# include <bag2rgbdepth.h>

void RGBCallback(const sensor_msgs::ImageConstPtr& msg){
    cv::Mat image;
    cv_bridge::CvImagePtr cv_ptr;
    if ( firstDepth )
    {
        try{
            cv_ptr = cv_bridge::toCvCopy(msg, msg->encoding);
        }
        catch (cv_bridge::Exception& e){
            ROS_ERROR("cv_bridge exception RGB: %s", e.what());
            return ;
        }
    }
    std::string filename = "rgb_" + std::to_string(rgbImages) + ".jpg" ;
    cv::imwrite("rgb.jpg",cv_ptr->image);
    firstRGB = true ;
}
void DepthCallback(const sensor_msgs::ImageConstPtr& msg){
    cv::Mat image;
    cv_bridge::CvImagePtr cv_ptr;
    if ( firstRGB ){
        try{
            cv_ptr = cv_bridge::toCvCopy(msg, sensor_msgs::image_encodings::TYPE_16UC1);
        }
        catch (cv_bridge::Exception& e){
            ROS_ERROR("cv_bridge exception DEPTH: %s", e.what());
            return ;
        }
    }
    std::string filename = "depth_" + std::to_string(depthImages) + ".jpg";
    // cv::imwrite("septh.jpg" ,cv_ptr->image);
    firstDepth = true;
}

int main(int argc, char** argv)
{
    ros::init(argc,argv,"bag2Depth");
    ros::NodeHandle nh;
    image_transport::ImageTransport it(nh);
    ROS_INFO("Running");
    // it.subscribe("/camera/rgb/image_raw", 1, RGBCallback);
    image_transport::CameraSubscriber subrgb = it.subscribeCamera("/camera/rgb/image_raw",1, boost::bind(&RGBCallback, _1));
    image_transport::CameraSubscriber subdepth = it.subscribeCamera("/camera/depth_registered/image_raw",1, boost::bind(&DepthCallback, _1));
    ROS_INFO("Spinning");
    ros::spin();

    return 0;
}