# Bag to Depth and RGB
This code is usefull for grabbing RGB and depth data from BAG file of ros in python and C++

The Python Code saves in both jpg and numpy pickle. Where as the C++ Code saves only in jpg

## What is needed
- A good installation of ROS
- Numpy 
- python 
- CVbridge

## How to execute ?
### Pre-Run requirements
#### Python Code
``` shell
cd src/bag2rgbdepth/scripts/
```
Arange the bag files in diffrent folders for each bag file as below
- Bag folder1
   - bagfile1.bag
- Bag folder2
   - bagfile2.bag
- grabrgb.py
- grabdepth.py
- truedepthandrgb.sh
### How to run
step 1: Run ros.sh using ``` sh ros.sh ``` on one terminal

step 2: Open another terminal and run ``` sh truedepthandrgb.sh ```

step 3: Wait

### What after it executes
The folder strcture now will be 
- Bag folder1
  - bagfile.bag
  - depth_images1
    - dframe1.jpg
    - dframe1.npy
    - ...
    - dframen.jpg
    - dframen.npy
  - rgb_images1
    - frame1.jpg
    - frame1.npy
    - ...
    - framen.jpg
    - framen.npy
- Bag folder2
  - bagfile2.bag
  - depth_images1
    - dframe1.jpg
    - dframe1.npy
    - ...
    - dframen.jpg
    - dframen.npy
  - rgb_images1
    - frame1.jpg
    - frame1.npy
    - ...
    - framen.jpg
    - framen.npy

#### C++
First you will need to build the code

##### Pre-Reqs
* OpenCV 3
* ROS desktop full
* C++ Compiler

Open launch file in `launch` folder
``` shell
vim Bag_to_Depth/src/bag2rgbdepth/launch/extractbag_to_rgbd.launch
```

Edit the line where it says

``` xml
<param name="folder_extract_location" value="./"/>
```

Change the `value` to the folder where you need to extract the images. The code will add the rgb and depth files.


Excute the below bash script 
``` shell
cd Bag_to_Depth/
catkin_make
source devel/setup.bash
roslaunch bag2rgbdepth extractbag_to_rgbd.launch
```

Meanwhile in another terminal run these two commands
``` shell
roscore &
rosbag play bagfile1.bag
```

### What after it executes
The folder strcture now will be 
- Bag folder1
  - bagfile.bag
  - depth_images1
    - dframe1.jpg
    - ...
    - dframen.jpg
  - rgb_images1
    - frame1.jpg
    - ...
    - framen.jpg

