# Capstone Project: Detecting types of vehicles on Singapore roads with Object Detection models to aid in road maintenance planning.

## Acknowledgement

### Data source
Traffic images were scraped during the period of **20 March 2021** from **0000 to 2359 hours** periodic at 1 minute intervals via Data.gov.sg by running my own scrap_lta_cctv.py file which would make a web API call to **data.gov.sg** via https://api.data.gov.sg/v1/transport/traffic-images. Details on the parameters returned from the API can be referenced in the following link: [Traffic images](https://data.gov.sg/dataset/traffic-images). 

Data was tidied up and stored under LTAdatasets folder(available on Google Drive for download) which are grouped in folders by CCTV IDs representing different CCTV locations in Singapore, (eg. 1001). The tidied dataset can be downloaded via [dataset link](https://drive.google.com/file/d/1LMBT6EU_hvXWR03-rN32gkxA-RTf76_Q/view?usp=sharing). Upon downloading, please extract and place it in the working directory where the repo is cloned. There would be 87 folders (identified by 4 digit identifiers) containing traffic footages of a particular location.

In each subfolders, it contains subfolders named *annotate* and *unannotate* CCTV footages. In the *annotate* subfolder, there are **100** images which comprises **50** images representing traffic footages from **6AM to 10AM** period and another **50** images representing traffic footages from 6PM to 10PM period. All other time periods traffic footages are stored in "unannotate" folder. 

Due to time constraints, only **27** CCTV IDs, each comprising 100 images in the annotated subfolders were manually annotated by myself for model training purposes during the course in Apr 2021. **Please note that the images are not in HD format and hence images maybe blurry at some time periods due to environment factors.** 

Stitched video of images from the **27** stated CCTV IDs are available for download if you want to test out the model for inference on video instead.[Stitched video download] (https://drive.google.com/file/d/1hgiw6rlvBf9W1ApU4UIFBbEjAiQC1xoT/view?usp=sharing)

The annotated IDs are:
- 1001 to 1006 (inclusive)
- 1501 to 1505 (inclusive)
- 2701 to 2705 (inclusive) and 2708
- 3702, 3704 and 3705
- 8701, 8702, 8704 and 8706
- 9704, 9705 and 9706
- 2706 (Added in Sep 2022. Stitched video not included)
(*Update: As a result, total 28 CCTV IDs are used for annotations*)

## Camera ID geolocations information as of 13 Dec 2022. [Update]
Alternatively, you may refer to the file *camera_coordinates.csv*
---
|ID|Lat|Lon|Description of Location|
|---|---|---|---|
|1001|1.29531332|103.871146|ECP/MCE/KPE instersection|
|1002|1.319541067|103.8785627|PIE(Tuas) exit road to KPE(MCE)|
|1003|1.323957439|103.8728576|PIE(Changi) exit road to KPE(TPE)|
|1004|1.319535712|103.8750668|PIE(Changi) exit to KPE(TPE)/Sims Way|
|1005|1.363519886|103.905394|KPE(TPE) Defu Flyover|
|1006|1.357098686|103.902042|KPE(MCE) Tunnel Entrance| 
|1501|1.274143944|103.8513168|Straits Boulevard to MCE|
|1502|1.271350907|103.8618284|Slip Road to MCE from Marina Link|
|1503|1.270664087|103.8569779|MCE(KPE) near Slip road to Central Boulevard|
|1504|1.294098914|103.8760562|Slip Road from ECP(Sheares) to MCE(AYE)|
|1505|1.275297715|103.8663904|Slip Road from Marina Coastal Drive to MCE(KPE)|
|1701|1.323604823|103.8587802|CTE Whampoa River|
|1702|1.34355015|103.8601984|CTE Braddell Flyover|
|1703|1.328147222|103.8622033|CTE Whampoa Flyover|
|1704|1.285693989|103.8375245|CTE/Chin Swee Road|
|1705|1.375925022|103.8587986|CTE Ang Mo Kio Flyover|
|1706|1.38861|103.85806|CTE Yio Chu Kang Flyover|
|1707|1.280365843|103.8304511|AYE(Tuas) Jalan Bukit Merah Exit|
|1709|1.313842317|103.845603|CTE(AYE) Cavenagh Exit|
|1711|1.35296|103.85719|CTE Ang Mo Kio South Flyover|
|2701|1.447023728|103.7716543|Causeway|
|2702|1.445554109|103.7683397|BKE Entrance after Causeway|
|2703|1.350477908|103.7910336|BKE/PIE Intersection|
|2704|1.429588536|103.769311|BKE Woodlands Flyover|
|2705|1.36728572|103.7794698|BKE Dairy Farm Flyover|
|2706|1.414142|103.771168|BKE Between Turf Club and Mandai Road exits|
|2707|1.3983|103.774247|BKE Between KJE and Mandai Road exits|
|2708|1.3865|103.7747|BKE(Woodlands) before Slip road to KJE|
|3702|1.33831|103.98032|ECP/PIE(Changi) Intersection|
|3704|1.295855016|103.8803147|ECP(Changi)/Slip Road from MCE to ECP(Changi)|
|3705|1.32743|103.97383|ECP(Sheares) Before Xilin Ave exit|
|3793|1.309330837|103.9350504|ECP Laguna Flyover|
|3795|1.301451452|103.9105963|ECP Marina Parade Flyover|
|3796|1.297512569|103.8983019|ECP Tanjong Katong Flyover|
|3797|1.295657333|103.885283|ECP Tanjong Rhu Flyover|
|3798|1.29158484|103.8615987|ECP Benjamin Sheares Bridge over Raffles Boulevard|
|4701|1.2871|103.79633|AYE Before Portsdown Flyover|
|4702|1.27237|103.8324|AYE Keppel Viaduct|
|4703|1.348697862|103.6350413|AYE After Tuas Checkpoint|
|4704|1.27877|103.82375|AYE Lower Delta Flyover|
|4705|1.32618|103.73028|AYE(MCE) after Yuan Ching Road Exit|
|4706|1.29792|103.78205|AYE(Tuas) After Buona Vista Flyover|
|4707|1.333446481|103.6527008|AYE(MCE) beside Jalan Ahmad Ibrahim|
|4708|1.29939|103.7799|AYE(MCE) beside Singapore Institute of Technology|
|4709|1.312019|103.763002|AYE(Tuas) before Exit to Clementi Ave 6|
|4710|1.32153|103.75273|AYE Pandan River Flyover|
|4712|1.341244001|103.6439134|AYE Jalan Ahmad Ibrahim slip road entrance/exit|
|4713|1.347645829|103.6366955|AYE Before Tuas Checkpoint|
|4714|1.31023|103.76438|AYE(Tuas) After Clementi Flyover|
|4716|1.32227|103.67453|AYE(Tuas) After Benoi Flyover|
|4798|1.259999997|103.8236111|Sentosa Gateway to Harbourfront|
|4799|1.260277774|103.8238889|Sentosa Gateway (Entrance/Exit to Sentosa)|
|5794|1.3309693|103.9168616|PIE(Tuas) After Bedok North Flyover|
|5795|1.326024822|103.905625|PIE Eunos Flyover|
|5797|1.322875288|103.8910793|PIE Paya Lebar Flyover|
|5798|1.320360781|103.8771741|PIE Aljunied West Flyover|
|5799|1.328171608|103.8685191|PIE Woodsville Flyover|
|6701|1.329334|103.858222|PIE(Tuas) Exit to Kim Keat Link|
|6703|1.328899|103.84121|PIE Thomson Flyover|
|6704|1.326574036|103.8268573|PIE Mount Pleasant Flyover|
|6705|1.332124|103.81768|PIE(Changi) after Adam Flyover|
|6706|1.349428893|103.7952799|PIE(Changi) after BKE exit|
|6708|1.345996|103.69016|PIE Nanyang Flyover|
|6710|1.344205|103.78577|PIE(Changi) Anak Bukit Flyover|
|6711|1.33771|103.977827|PIE(Changi) Exit from ECP|
|6712|1.332691|103.7702788179709|PIE(Tuas) before slip road to Clementi Ave 6|
|6713|1.340298|103.945652|PIE(Tuas) after Tampines South Flyover|
|6714|1.361742|103.703341|PIE(Changi) exit to KJE(BKE)
|6715|1.356299|103.716071|PIE Hong Kah Flyover|
|6716|1.322893|103.6635051|AYE/PIE Tuas Flyover|
|7791|1.354245|103.963782|TPE Upper Changi Flyover|
|7793|1.37704704|103.9294698|TPE Api Api Flyover|
|7794|1.37988658|103.9200917|TPE(SLE) slip road to KJE|
|7795|1.38432741|103.915857|TPE(Changi) after Halus Bridge|
|7796|1.39559294|103.9051571|TPE(SLE) before Punggol Flyover|
|7797|1.40002575|103.8570253|TPE/Seletar West Link Intersection|
|7798|1.39748842|103.8540047|TPE(SLE) exit to SLE|
|8701|1.38647|103.74143|KJE Choa Chu Kang West Flyover|
|8702|1.39059|103.7717|KJE Gali Batu Flyover|
|8704|1.3899|103.74843|KJE(BKE) After Choa Chu Kang Dr|
|8706|1.3664|103.70899|PIE(Tuas) Slip Road to KJE|
|9701|1.39466333|103.834746|SLE Lentor Flyover|
|9702|1.39474081|103.8179709|SLE Upper Thomson Flyover|
|9703|1.422857|103.773005|SLE/BKE Interchange|
|9704|1.42214311|103.7954206|SLE Ulu Sembawang Flyover|
|9705|1.42627712|103.7871664|SLE Marsiling Flyover|
|9706|1.41270056|103.8064271|SLE Mandai Lake Flyover|



### Annotation tool used for annotating data: Makesense.ai
- Web link to annotation tool: [Makesense.ai](https://www.makesense.ai/)
- *labels.txt* file containing the general vehicle classes is used for annotation (car, lorry_truck, van, bike and bus)
- Annotations are made on vehicles in the footages which are identifiable by human eye and in about 50-75% of the foreground of the images.

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
The results of my model inference for each model trained are located in folders under darknet/backup directory. A mean average precision of 48% was achieved using **YOLOv4** model with default hyperparameter configuration and this value was calculated based on 501 validation images out of 516 validation image (97.1%) detection rate. In view of the large amount of unannotated data that could be used for training, I believe the inclusion of those data with corresponding annotations could potentially push the mean average precision above 50% when there is proper pre-processing as well as optimal hyperparameter tuning.

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


## Trained **YOLOv4** model weights
You may download the model weights that were saved during the process of training from the following link. [Trained_weights](https://drive.google.com/file/d/107W85LuYDNhOcZdQ6jXGrlYnUTqPlXQI/view?usp=sharing). 

Extract the folders and place them into `darknet/backup` folder after darknet folder has been cloned into the repository to facilitate model inference using trained-weights.

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

