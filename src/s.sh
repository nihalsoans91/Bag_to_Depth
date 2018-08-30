#!/bin/bash

hm=/home/kbogert/test_videos

#cd "$hm"/data

sudo chmod -R 777 "$hm"

for d in */;
  do 
     echo Entering into $d
     listf=`ls "$d"| grep rgbdepth`
     echo ${listf}
     cd "$d"
     i=1
     for f in ${listf} ; do
	     mkdir rgb_images$i
	     cd rgb_images$i
	     echo "Doing RGB"
	     ps aux | grep rosbag | grep -v grep | awk '{print $2}' | xargs kill -SIGKILL > /dev/null 2>&1
	     ps aux | grep rosrun | grep -v grep | awk '{print $2}' | xargs kill -SIGKILL > /dev/null 2>&1
	     ps aux | grep image_view | grep -v grep | awk '{print $2}' | xargs kill -SIGKILL > /dev/null 2>&1
	     #rosrun image_view image_saver image:=/camera/rgb/image_raw > /dev/null 2>&1 &
	     rosrun image_view video_recorder image:=/camera/rgb/image_raw > /dev/null 2>&1 &
	     rosbag play ../$f > /dev/null 2>&1 &
	     #rosbag play ../rgbdepth*.bag & #> /dev/null 2>&1 &
	     #PID=$!
	     #sleep 2
	     #kill $PID
	     sleep 15
	     ps aux | grep rosbag | grep -v grep | awk '{print $2}' | xargs kill -SIGKILL > /dev/null 2>&1
	     ps aux | grep rosrun | grep -v grep | awk '{print $2}' | xargs kill -SIGKILL > /dev/null 2>&1
	     ps aux | grep image_view | grep -v grep | awk '{print $2}' | xargs kill -SIGKILL > /dev/null 2>&1
	     cd ..
	     mkdir depth_images$i
	     cd depth_images$i
	     echo "Doing Depth"
	     #rosrun image_view video_recorder image:=/camera/depth_registered/image > /dev/null 2>&1 &
	     rosrun image_view image_saver image:=/camera/depth_registered/image > /dev/null 2>&1 &
	     rosbag play ../$f > /dev/null 2>&1 &
	     #rosbag play ../rgbdepth*.bag & #> /dev/null 2>&1 &
	     sleep 15
	     ps aux | grep rosbag | grep -v grep | awk '{print $2}' | xargs kill -SIGKILL > /dev/null 2>&1
	     ps aux | grep rosrun | grep -v grep | awk '{print $2}' | xargs kill -SIGKILL > /dev/null 2>&1
	     ps aux | grep image_view | grep -v grep | awk '{print $2}' | xargs kill -SIGKILL > /dev/null 2>&1
	     cd ..
	     i=$((i+1))
     done;
     cd ..
done;
