# bag2rgbdepth

A ROS package for extracting RGB and depth image frames from `.bag` files. Frames are saved as both JPEG (for viewing) and NumPy `.npy` arrays (for processing). Available as both Python scripts and a C++ ROS node.

---

## Prerequisites

| Dependency | Version |
|---|---|
| ROS | Kinetic / Melodic / Noetic |
| Python | 3.6+ |
| OpenCV | 3.x or 4.x |
| NumPy | any recent |
| cv_bridge | (included with ROS desktop-full) |

---

## Installation

### Python scripts

No build step required. The scripts in `src/bag2rgbdepth/scripts/` can be run directly.

### C++ node

```bash
cd Bag_to_Depth/
catkin_make
source devel/setup.bash
```

---

## Usage

### Option A — Synchronized RGB + depth (single bag pass)

This is the recommended approach. Both streams are captured simultaneously.

**1.** Start `roscore` in a separate terminal:
```bash
roscore
```

**2.** Run the batch extraction script from the directory containing your bag folders:
```bash
cd /path/to/bag/folders
sh /path/to/scripts/truedepthandrgb_sync.sh
```

Expected folder layout before running:
```
session1/
  recording.bag
session2/
  recording.bag
truedepthandrgb_sync.sh   <- run from here
```

---

### Option B — Separate RGB and depth passes

Plays each bag twice: once for RGB, once for depth. Use this if the synchronized script has timing issues.

```bash
cd /path/to/bag/folders
sh /path/to/scripts/truedepthandrgb.sh
```

---

### Option C — Single-script usage

Run any grabber manually against a specific output folder:

```bash
# RGB only
python3 grabrgb.py /output/rgb_folder

# Depth only
python3 grabdepth.py /output/depth_folder

# Both simultaneously
python3 grabrgbdepth.py /output/rgb_folder /output/depth_folder
```

Then in a separate terminal, play your bag:
```bash
rosbag play recording.bag
```

---

### Option D — C++ ROS node

Edit the output path in the launch file:
```bash
vim src/bag2rgbdepth/launch/extractbag_to_rgbd.launch
```

Change `value` to your desired output directory:
```xml
<param name="folder_extract_location" value="/path/to/output"/>
```

Launch the node, then play your bag:
```bash
# Terminal 1
roslaunch bag2rgbdepth extractbag_to_rgbd.launch

# Terminal 2
rosbag play recording.bag
```

---

## Output structure

After extraction each bag folder will contain:

```
session1/
  recording.bag
  rgb_images1/
    frame0.jpg       <- BGR color image
    frame0.npy       <- raw uint8 BGR array
    frame1.jpg
    frame1.npy
    ...
  depth_images1/
    dframe0.jpg      <- 8-bit normalized depth (for viewing)
    dframe0.npy      <- raw uint16 depth values in mm
    dframe1.jpg
    dframe1.npy
    ...
```

> **Note:** The C++ node saves depth as 16-bit PNG (`depth_N.png`) instead of JPEG, preserving full depth precision.

---

## ROS topics

The default topics match a standard OpenNI/RealSense camera:

| Topic | Type | Description |
|---|---|---|
| `/camera/rgb/image_raw` | `sensor_msgs/Image` | Color stream |
| `/camera/depth_registered/image_raw` | `sensor_msgs/Image` | Registered depth stream |

---

## Duplicate frame filtering

All grabbers skip saving frames that are identical to the previous saved frame. This avoids redundant images when the bag is paused or the camera feed is static.
