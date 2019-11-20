# include <bag2rgbdepth.h>

void RGBCallback(const sensor_msgs::ImageConstPtr& msg){
    cv::Mat image;
    
    if ( firstDepth )
    {
        try{
            cv_ptr_rgb = cv_bridge::toCvCopy(msg, "bgr8");
        }
        catch (cv_bridge::Exception& e){
            ROS_ERROR("cv_bridge exception RGB: %s", e.what());
            return ;
        }
        std::string filename = filename_home + "/rgb/rgb_" + std::to_string(rgbImages) + ".jpg" ;
        cv::imwrite(filename,cv_ptr_rgb->image);
        rgbImages++;
    }
    firstRGB = true ;
}
void DepthCallback(const sensor_msgs::ImageConstPtr& msg){
    cv::Mat image;
    cv_bridge::CvImagePtr cv_ptr_depth;
    if ( firstRGB ){
        try{
            cv_ptr_depth = cv_bridge::toCvCopy(msg, sensor_msgs::image_encodings::TYPE_16UC1);
        }
        catch (cv_bridge::Exception& e){
            ROS_ERROR("cv_bridge exception DEPTH: %s", e.what());
            return ;
        }
        std::string filename = filename_home + "depth/depth_" + std::to_string(depthImages) + ".jpg";
        cv::imwrite(filename ,cv_ptr_depth->image);
        depthImages++;
    }
    firstDepth = true;
}

int main(int argc, char** argv)
{
    ros::init(argc,argv,"bag2Depth");
    ros::NodeHandle nh;
    image_transport::ImageTransport it(nh);
    nh.getParam("folder_extract_location",filename_home);
    std::string filergb = filename_home+"/rgb";
    std::string filedepth = filename_home+"/depth";
    mkdir(filergb.c_str(),0777);
    mkdir(filedepth.c_str(),0777);
    cv_ptr_rgb.reset (new cv_bridge::CvImage);
    ROS_INFO("Running");
    // it.subscribe("/camera/rgb/image_raw", 1, RGBCallback);
    subrgb = it.subscribeCamera("/camera/rgb/image_raw",1, boost::bind(&RGBCallback, _1));
    subdepth = it.subscribeCamera("/camera/depth_registered/image_raw",1, boost::bind(&DepthCallback, _1));
    ROS_INFO("Spinning");
    ros::spin();

    return 0;
}