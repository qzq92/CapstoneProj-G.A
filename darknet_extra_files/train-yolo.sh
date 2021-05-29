#!/usr/bin/bash

echo "Running YOLO training"
./darknet detector train data/lta.data cfg/yolov4-lta.cfg -map
