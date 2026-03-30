#!/bin/bash
set -euo pipefail

SCRIPTS_DIR="$(cd "$(dirname "$0")" && pwd)"

for d in */; do
    echo "Processing directory: $d"
    bag_files=$(ls "$d"*.bag 2>/dev/null || true)
    if [ -z "$bag_files" ]; then
        echo "  No .bag files found in $d, skipping."
        continue
    fi

    i=1
    for f in $bag_files; do
        rgb_out="$d/rgb_images$i"
        depth_out="$d/depth_images$i"
        mkdir -p "$rgb_out" "$depth_out"

        echo "  Extracting RGB+depth from $f"
        python3 "$SCRIPTS_DIR/grabrgbdepth.py" "$rgb_out" "$depth_out" &
        GRABBER_PID=$!
        rosbag play "$f"
        sleep 2
        kill "$GRABBER_PID" 2>/dev/null || true

        i=$((i + 1))
    done
done

echo "Done."
