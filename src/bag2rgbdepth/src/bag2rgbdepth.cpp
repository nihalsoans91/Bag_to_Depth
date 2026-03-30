#include <bag2rgbdepth.h>

bool firstRGB = false;
bool firstDepth = false;
uint64_t rgbImages = 0;
uint64_t depthImages = 0;
image_transport::CameraSubscriber subdepth;
image_transport::CameraSubscriber subrgb;
cv_bridge::CvImagePtr cv_ptr_rgb;
std::string filename_home = "";

void RGBCallback(const sensor_msgs::ImageConstPtr& msg)
{
    if (!firstDepth)
        return;

    try {
        cv_ptr_rgb = cv_bridge::toCvCopy(msg, "bgr8");
    } catch (cv_bridge::Exception& e) {
        ROS_ERROR("cv_bridge RGB exception: %s", e.what());
        return;
    }

    std::string filename = filename_home + "/rgb/rgb_" + std::to_string(rgbImages) + ".jpg";
    cv::imwrite(filename, cv_ptr_rgb->image);
    ROS_INFO("Saved RGB frame %lu", rgbImages);
    rgbImages++;
    firstRGB = true;
}

void DepthCallback(const sensor_msgs::ImageConstPtr& msg)
{
    if (!firstRGB)
        return;

    cv_bridge::CvImagePtr cv_ptr_depth;
    try {
        cv_ptr_depth = cv_bridge::toCvCopy(msg, sensor_msgs::image_encodings::TYPE_16UC1);
    } catch (cv_bridge::Exception& e) {
        ROS_ERROR("cv_bridge depth exception: %s", e.what());
        return;
    }

    std::string filename = filename_home + "/depth/depth_" + std::to_string(depthImages) + ".png";
    cv::imwrite(filename, cv_ptr_depth->image);
    ROS_INFO("Saved depth frame %lu", depthImages);
    depthImages++;
    firstDepth = true;
}

int main(int argc, char** argv)
{
    ros::init(argc, argv, "bag2Depth");
    ros::NodeHandle nh;
    image_transport::ImageTransport it(nh);

    nh.getParam("folder_extract_location", filename_home);
    ROS_INFO("Output folder: %s", filename_home.c_str());

    mkdir((filename_home + "/rgb").c_str(), 0755);
    mkdir((filename_home + "/depth").c_str(), 0755);

    subrgb   = it.subscribeCamera("/camera/rgb/image_raw", 1,
                                   boost::bind(&RGBCallback, _1));
    subdepth = it.subscribeCamera("/camera/depth_registered/image_raw", 1,
                                   boost::bind(&DepthCallback, _1));

    ROS_INFO("Listening for RGB and depth frames...");
    ros::spin();

    ROS_INFO("Done. Saved %lu RGB frames and %lu depth frames.", rgbImages, depthImages);
    return 0;
}
