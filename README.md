# Capstone Project: Detecting types of vehicles on Singapore roads with Object Detection models to aid in road maintenance planning.

## Acknowledgement

### Data source
Traffic images were scraped on 20 March 2021 from 0000 to 2359 hours periodic at 1 minute intervals via Data.gov.sg by running my own scrap_lta_cctv.py file which would make a web API call to data.gov.sg via https://api.data.gov.sg/v1/transport/traffic-images. Details on the parameters returned from the API: [Traffic images](https://data.gov.sg/dataset/traffic-images). 

Data was tidied up and stored under LTAdatasets folder grouped by CCTV IDs folders, (eg. 1001). 

In each subfolders, it contains subfolders of annotate and unannotate CCTV footages. In the annotate subfolder, there are 100 images which comprises 50 images representing traffic footages from 6AM to 10AM period and the other 50 images representing traffic footages from 6PM to 10PM period. All other time periods traffic footages are stored in unannotate. 

Due to time constraints, only 27 CCTV IDs comprising of 100 images in the annotated subfolders were actually annotated.
The IDs are:
- 1001 to 1006 (inclusive)
- 1501 to 1505 (inclusive)
- 2701 to 2705(inclusive) and 2708
- 3702, 3704 and 3705
- 8701, 8702, 8704 and 8706
- 9704, 9705 and 9706

### Annotation tool used for annotating data: Makesense.ai
- Web link to annotation tool: [Makesense.ai](https://www.makesense.ai/)

### Codes and repositories required
- Darknet framework for object detection work: [Darknet](https://github.com/AlexeyAB/darknet) - To be manually cloned onto this repository subsequently.
- Mean Average Precision evaluation: [mAP](https://github.com/Cartucho/mAP) - Modified version provided in this repository
- Open Source Computer Vision Library: [OpenCV](https://github.com/opencv/opencv) - To be manually cloned onto this repository subsequently.

## Setup
Please refer to the environment setup section below. You may need to clone Darknet repository as the implementation of model used for training is reference from the guide inside the Darknet repository. In addition, there maybe a need to download pre-trained model weights online to facilitate model training on the dataset if you need to train your own model.

## Background
In Singapore, there are about 1 million vehicles that is on our road network of more than 9,000 lane-kilometres which constitutes up to 12% of our land and road maintenance is currently maintained by Land Transport Authority (LTA). It has been known that roads, and means of transport, make a crucial contribution to economic development and growth and bring important social benefits, which is extremely important for Singapore. Reference: [Ministry of Transport, Singapore](https://www.mot.gov.sg/About-MOT/Land-Transport/Motoring/Road-Network/)

## Problem statement
In view of the periodic maintenance regime that includes periodic road inspections and surveys that were planned by LTA, we could also leverage AI related technology to better assist LTA in their road maintenance regime. As such, I had developed a vehicle recognition model through the use of AI object detection techniques to aid in detecting and classifying the number of vehicle types traveled on Singapore roads across various time periods of the day, which could potentially supplement as an additional source of information for planning road maintenance regime.

## Summary of Findings & Recommendations
---
The results of my model inference for each model trained are located in folders under darknet/backup directory. A mean average precision of 48% was achieved using YOLOv4 model with default hyperparameter configuration and this value was calculated based on 501 validation images out of 516 validation image (97.1%) detection rate. In view of the large amount of unannotated data that could be used for training, I believe the inclusion of those data with corresponding annotations could potentially push the mean average precision above 50% when there is proper pre-processing as well as optimal hyperparameter tuning.

## Sample predictions 1 (Top: Manual labelled, Bottom: Vehicle detected by model) 
![Alt text](sample_output2.png?raw=true)

## Sample predictions 2 (Screenshot of model inference implemented on a video clip) 
![Alt text](model_inference.png?raw=true)

## Future work
1. Continuation of image labelling
2. Retraining of models

## Data Dictionary of annotation made using makesense.ai
---
|Feature|Type|Description|
|---|---|---|
|**Column 1**|*object*|Vehicle types: either Car, Lorry_Truck, van, bike or bus| 
|**Column 2**|*int*|bounding box top left x coordinates|
|**Column 3**|*int*|bounding box top left y coordinates|
|**Column 4**|*int*|US State average ACT score for Reading subject for 2017|
|**Column 5**|*object*|bounding box height|
|**Column 6**|*object*|bounding box height|
|**Column 7**|*filename*|Image width|
|**Column 8**|*filename*|Image height|

# Environment setup 
Please follow the steps below to setup your environment for model training with Darknet's YOLO framework

## Pre-requisites:
- CUDA and CuDnn (CUDA 11.0 and CUDNN 8.0.4 were installed and used during development) if you have GPU
- Internet connection
- Activated conda environment

## Useful Git related tools
- git (tool for code versioning) 
- git-lfs (tool to extend git for versioning large files) --Optional

## Dataset download link
Please download the dataset represented with LTAdatasets.zip from the following link: [Dataset download link](https://drive.google.com/file/d/16oQZaxut5It0w1zQXFlTTB1gB6jktqAy/view?usp=sharing).

Unzip the file and you will see 87 folders with 4 digit identifier containing traffic footages of a particular location.

## Trained YOLOv4 model weights
You may download the model weights that were saved during the process of training from the following link. [Trained_weights](https://drive.google.com/file/d/107W85LuYDNhOcZdQ6jXGrlYnUTqPlXQI/view?usp=sharing). 

Extract the files and put them into darknet/backup folder after darknet folder has been cloned into the repository to facilitate model inference using trained-weights.

# Installation of libraries

## Install opencv package for reading images
1. Activate environment and run the following command to install opencv environment
```
$ conda install -c conda-forge opencv
```

## Setting up binaries for YOLO framework 
Refer to the medium article for installation of opencv for yolov4. [Article link](https://medium.com/nerd-for-tech/install-opencv-from-source-for-yolov4-for-ubuntu-ccfa9405a3c3)

## Install Cmake, gcc and g++ with supported version by adding Kitware signing key and add repository to linux source list
```
$ wget -O - https://apt.kitware.com/keys/kitware-archive-latest.asc 2>/dev/null | gpg --dearmor - | sudo tee /etc/apt/trusted.gpg.d/kitware.gpg >/dev/null
$ sudo apt-add-repository 'deb https://apt.kitware.com/ubuntu/ bionic main'
$ sudo apt update
$ sudo apt-get install cmake (installed 3.10.2-1ubuntu2.18.04.1)
$ sudo apt-get install gcc g++ (installed 4:7.4.0-1ubuntu2.3)
```

## If you want to remove previous CMake installation
```
$ sudo apt purge --auto-remove cmake
```

## OpenCV download and installation
Installing numpy on host that is required for opencv
```
$ sudo apt-get install python3-dev python3-numpy
$ git clone https://github.com/opencv/opencv.git
$ cd opencv
$ mkdir build
$ cd build
$ cmake ../
$ make
$ sudo make install
```

## Install binaries for opencv
```
$ sudo apt-get install libopencv-dev
```

Check opencv binary version (should be at least 4.5.2-dev as of writing)
```
$ opencv_version
```

Please adjust the settings in makefile based on your PC specs and run make. 
Ensure the path for pkgconfig is set: PKG_CONFIG_PATH=$PKG_CONFIG_PATH:"/usr/local/lib/pkgconfig"

## Compile & install Darknet (requires cmake version 3.18 and higher).
Follow the setup instructions as stated in the repository of AlexeyAB using the link below. For my case, I referred to the `make` section to compile and install darknet framework. 

The repository also provides information on how to tune parameters for model training, as well as downloadable pre-train weights for YOLO models. Please follow the steps in downloading the weights and move them to the darknet folder. Link to Darknet repository as follows:
[Darknet](https://github.com/AlexeyAB/darknet#requirements)

**Important notes:** 
By cloning the darknet directory, it comes with the LTA data that I have placed in YOLO darknet/data/obj directory where it has been already split into train and test folder. You should not need to modify lta_train.txt and lta_validation.txt as they point to the image files using relative paths which is required to train YOLO model.


## Additional things to be copied over from `darknet_extra_files` if you are cloning Darknet repository directly from official source.
1. All cfg files inside should be inside darknet/cfg folder

2. Copy over the obj folder into darknet/data folder.

3. lta.data and lta.names should be copied into darknet/data folder. No change in content is required as relative path are used.

4. Pre-trained YOLO weights can be downloaded by referencing the README in the actual darknet repository, which is accessible from the hyperlink provided above. Alternatively, to train YOLOv3 and YOLOv4 models, you can run the following commands:
```
- $ wget https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/yolov4.weights

- $ wget https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/yolov4.conv.137
```
5. Copy over demo.sh into darknet folder to run inference with trained weights on a stiched mp4 video. This would work only if darknet is successfully setup on your computer. Otherwise, error would be flagged. Example of the command is as follows 
```
./darknet detector demo data/lta.data backup/default10k_416wh/yolov4-lta.cfg backup/default10k_416wh/yolov4-lta_best.weights ../LTAdatasets/1711/lta_image_video_1711.mp4 -ext_output
```

# Troubleshooting:
1. In case of Errors during make indicating opencv not found in pkg-config during building darknet process. Run following command:
```
$ apt-file search opencv.pc
$ sudo apt-get install -y libopencv-dev
$ pkg-config --cflags opencv
$ pkg-config --libs opencv
```

2. Package opencv was not found in the pkg-config search path.
```
$ sudo apt-get install libopencv-dev
```

3. nvcc: not found
Add the path to your cuda folder as PATH variable: 
Eg. in ~/.bashrc add PATH=/usr/local/cuda/bin:$PATH

