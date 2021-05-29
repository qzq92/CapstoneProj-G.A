#!/usr/bin/bash
./darknet detector demo data/lta.data backup/default10k_416wh/yolov4-lta.cfg backup/default10k_416wh/yolov4-lta_best.weights ../LTAdatasets/1711/lta_image_video_1711.mp4 -ext_output
