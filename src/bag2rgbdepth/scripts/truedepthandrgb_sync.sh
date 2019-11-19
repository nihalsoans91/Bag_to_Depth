#!/bin/bash

hm=./

#cd "$hm"/data

sudo chmod -R 777 "$hm"

for d in */;
  do 
     echo Entering into $d
     listf=`ls "$d"| grep .bag`
     echo ${listf}
     cd "$d"
     i=1
     for f in ${listf} ; do
             pwd
	     mkdir rgb_images$i
		 mkdir depth_images$i
	     echo "Doing RGB and Depth"
	     python2 ../grabrgbdepth.py rgb_images$i depth_images$i &
             pwd
	     rosbag play $f
	     sleep 15
	     ps aux | grep rosbag | grep -v grep | awk '{print $2}' | xargs kill -SIGKILL > /dev/null 2>&1
	     ps aux | grep grabrgb | grep -v grep | awk '{print $2}' | xargs kill -SIGKILL > /dev/null 2>&1
	     cd ..
	     i=$((i+1))
     done;
     cd ..
done;
