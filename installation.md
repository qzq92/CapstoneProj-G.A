# Environment setup 
Please follow the steps below to setup your environment for model training with Darknet's YOLO framework

# Pre-requisites:
- CUDA and CuDnn (CUDA 11.0 and CUDNN 8.0.4 were installed and used during development) if you have GPU
- Internet connection
- Activated conda environment

# Useful Git related tools
- git (tool for code versioning) 
- git-lfs (tool to extend git for versioning large files) --Optional

# Dataset download link
Please download the dataset represented with LTAdatasets.zip from the following link: [Dataset Download](https://drive.google.com/file/d/16oQZaxut5It0w1zQXFlTTB1gB6jktqAy/view?usp=sharing)
Unzip the file and you will see 87 folders with 4 digit identifier containing traffic footages of a particular location.

# Installation 

## Install opencv package for reading images
1. Activate environment and run the following command to install opencv environment
```
$ conda install -c conda-forge opencv
```

## Setting up binaries for YOLO framework 
[reference](https://medium.com/nerd-for-tech/install-opencv-from-source-for-yolov4-for-ubuntu-ccfa9405a3c3)

## Installing CMake and gcc g++ compilers on your computer
```
$ sudo apt-get install cmake
$ sudo apt-get install gcc g++
```

## Add Kitware signing key and add repository to linux source list
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

Check opencv binary version
```
$ opencv_version (4.5.2-dev)
```

Please adjust the settings in makefile based on your PC specs and run make. 
Ensure the path for pkgconfig is set: PKG_CONFIG_PATH=$PKG_CONFIG_PATH:"/usr/local/lib/pkgconfig"

## Compile & install Darknet (requires cmake version 3.18 and higher).
Follow the setup instructions as stated in the repository of AlexeyAB using the link below. It also provides information on how to tune parameters for model training. Pre-train weights for YOLO models are also found in the official repository, please follow the steps in downloading the weights and move them to the darknet folder.
[Darknet](https://github.com/AlexeyAB/darknet#requirements)

**Important notes:** 
By cloning the darknet directory, it comes with the LTA data that I have placed in YOLO darknet/data/obj directory where it has been already split into train and test folder. You should not need to modify lta_train.txt and lta_validation.txt as they point to the image files using relative paths which is required to train YOLO model.


# Additional things to be copied over from darknet_extra_files if you are cloning Darknet repository directly.
1. All cfg files inside should be inside darknet/cfg folder

2. Copy over the obj folder into darknet/data folder.

3. lta.data and lta.names should be copied into darknet/data folder. No change in content is required as relative path are used.

4. Pre-trained YOLO weights can be downloaded by referencing the README in the actual darknet repository, which is accessible from the hyperlink provided above. Alternatively, to train YOLOv3 and YOLOv4 models, you can run the following commands:
```
- $ wget https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/yolov4.weights

- $ wget https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/yolov4.conv.137
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

