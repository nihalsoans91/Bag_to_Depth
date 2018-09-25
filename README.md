# Bag to Depth and RGB
This code is usefull for grabbing RGB and depth data from BAG file of ros in python

## What is needed
- A good installation of ROS
- Numpy 
- python 
- CVbridge

## How to execute ?
### Pre-Run requirements
Arange the bag files in diffrent folders as below
- Bag folder1
   - bagfile.bag
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
    - frame1.jpg
    - frame1.npy
    - ...
    - framen.jpg
    - framen.npy
  - rgb_images1
    - frame1.jpg
    - frame1.npy
    - ...
    - framen.jpg
    - framen.npy
- Bag folder2
  - bagfile2.bag
  - depth_images1
    - frame1.jpg
    - frame1.npy
    - ...
    - framen.jpg
    - framen.npy
  - rgb_images1
    - frame1.jpg
    - frame1.npy
    - ...
    - framen.jpg
    - framen.npy
