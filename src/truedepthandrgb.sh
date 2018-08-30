#!/bin/bash

hm=./

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
	     python ../../grabrgb.py &
	     rosbag play ../$f
	     sleep 15
	     break
	     cd ..
	     mkdir depth_images$i
	     cd depth_images$i
	     echo "Doing Depth"
	     python ../../grabdepth.py
	     rosbag play ../$f &
	     sleep 15
	     cd ..
	     i=$((i+1))
     done;
     cd ..
done;
