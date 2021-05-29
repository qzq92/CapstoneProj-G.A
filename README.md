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

## Dataset download link
Please download the dataset represented with LTAdatasets.zip from the following link: [Dataset Download](https://drive.google.com/file/d/16oQZaxut5It0w1zQXFlTTB1gB6jktqAy/view?usp=sharing)

Unzip the file and you will see 87 folders with 4 digit identifier containing traffic footages of a particular location.

### Annotation tool used for annotating data: Makesense.ai
- Link to browser tool: [Makesense.ai](https://www.makesense.ai/)

### Codes and repositories
- Darknet framework for object detection work: [Darknet](https://github.com/AlexeyAB/darknet)
- Mean Average Precision evaluation: [mAP](https://github.com/Cartucho/mAP)
- Open Source Computer Vision Library: [OpenCV](https://github.com/opencv/opencv)

## Installation and Setup
Please refer to the installation.md file in the repository. You may need to clone Darknet repository as the implementation of model used for training is reference from the guide inside the Darknet repository. In addition, there maybe a need to download pre-trained model weights online to facilitate model training on the dataset if you need to train your own model.

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

## Trained YOLOv4 model weights
You may download the model weights that were saved during the process of training fromthe following link [trained_weights](https://drive.google.com/file/d/107W85LuYDNhOcZdQ6jXGrlYnUTqPlXQI/view?usp=sharing). 

Extract the files and put them into darknet/backup folder after darknet folder has been cloned into the repository to facilitate model inference using trained-weights.

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
