import os
import sys
import pandas as pd
import csv
import cv2
import matplotlib.pyplot as plt
import glob
import shutil
import time
import argparse
import subprocess
import logging

"""
This script is to be moved from archive folder to main directory of the repository.
"""

def process_annotation(src_annot_file, des_annot_file):
    """
    This function processes text file containing predicted bounding boxes and labels from darknet API in the form of
    <car: XX%\t (left_x:  XX   top_y:   YY   width:   WW   height:   HH)>
    and converts them to the following format `<class_name>` `<confidence>` `<left>` `<top>` `<right>` `<bottom>`
    required by mAP calculation by Cartucho repository : https://github.com/Cartucho/mAP
    """

    with open(src_annot_file, 'r') as in_file:
        # Identify milli-seconds wording as the predicted bounding box section
        # occurs the nextline
        bboxes_list = [line.strip() for line in in_file if "%" in line]

        #Assume that "%" only shows in predicted bounding boxes
        print(f"Predicted {len(bboxes_list)} objects for\n {src_annot_file}")

        image_name = src_annot_file.split("/")[-1]

        images_with_predictions = []
        images_without_predictions = []
        # Write annotations if there is at least 1 entry, otherwise skip.
        if len(bboxes_list):
            with open(des_annot_file, 'w') as out_file:
                writer = csv.writer(out_file)
                for entries in bboxes_list:
                    prediction, bbox = entries.split("\t")
                    prediction_label = prediction.split(":")[0]
                    confidence =  prediction.split(":")[1]
                    # Rename predictions if using old training weights trained on
                    # labels containing "lorry/truck".
                    if prediction == "lorry/truck":
                        prediction = "lorry_truck"
                    #Convert percentage to decimal
                    confidence = int(confidence.replace("%",""))/100

                    #Replace brackets with empty string and split by "  "
                    bbox =  bbox.replace("(", "").replace(")","").split("  ")

                    # Strip all empty spaces and remove empty string in above
                    # list created by split
                    bbox = [i.strip() for i in bbox if i!= ""]

                    # Calculate x_max = x_top_left + width,
                    # y_max = y_top_left + width
                    x_max = int(bbox[1]) + int(bbox[5])
                    y_max = int(bbox[3]) + int(bbox[7])
                    # Write the output based on described format
                    output = [str(prediction_label)+ " " +
                              str(confidence) + " " +
                              bbox[1] + " " +
                              bbox[3] + " " +
                              str(x_max) + " " +
                              str(y_max)]

                    #Write entries in format of prediction label,
                    #confidence value and predicted bounding boxes deta
                    writer.writerow(output)

def main():
    """
    Main function that runs when this script is run with python command.
    The function applies darknet detector bash command to run model inference on
    images from a provided input argument which generates text file for each
    image in darknet stipulated structure. The file is then processed by another
    function which removes unnecessary information from the text file and
    generates a processed version.

    The input folder, output folder for the processing and the weights for model
    inference are to be provided by the user running this script
    Processes the arguments fed in terminal/command prompt:

    @args.input_folder: relative path to folder where images are stored
    @args.output_directory: relative path to folder where processed text file
                            are to be stored
    @args.weights: relative path to darknet weights for use in model inference.
    """
    if not os.path.exists(args.input_folder):
        raise Exception("Invalid path. Please provide a valid relative path")

    if not os.path.exists(args.output_directory):
        os.makedirs(os.path.join(os.getcwd(),args.output_directory), "raw")

    output_dir = os.path.join(os.getcwd(),args.output_directory, "raw")

    if not os.path.exists(args.weights):
        raise Exception("Invalid path. Please provide a valid relative path")

    weights_path = os.path.join(os.getcwd(),args.weights)

    input_folder_directory = os.path.join(os.getcwd(), str(args.input_folder), "**")

    logging.info("Changing to darknet directory")
    os.chdir("./darknet")
    logging.info(f"Working in {os.getcwd()}")
    start_time = time.time()

    counter = 0
    for filename in glob.iglob(input_folder_directory, recursive=True):
        if os.path.isfile(filename) and filename.endswith(".jpg"): # filter directory
            counter += 1
            txt_for_img = filename.replace(".jpg", ".txt")
            img_name = txt_for_img.split("/")[-1]
            output_txt = os.path.join(output_dir, img_name)
            logging.info(f"Processing {counter}: {filename} and writing to {output_txt}")
            os.system(f"./darknet detector test data/lta.data cfg/yolov4-lta.cfg {weights_path} {filename} -ext_output > {output_txt}")
    # Calculate time to process
    time_elapsed = time.time() - start_time
    logging.info('{:.0f}m {:.0f}s'.format(time_elapsed // 60, time_elapsed % 60))



    logging.info("Changing to back to parent directory")
    os.chdir("../")
    logging.info(f"Working in {os.getcwd()}")


    src_dir = os.path.join(os.getcwd(), args.output_directory, "raw", "**")
    #Create an arbitrary folder named "processed" in specified output directory
    dest_dir = os.path.join(os.getcwd(), args.output_directory, "processed")

    #Remake directory by removing previous contents
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
        os.makedirs(dest_dir)
    else:
        os.makedirs(dest_dir)


    #Process each exported text file generated from darknet
    count = 0
    for predict_bbox_files in glob.iglob(src_dir, recursive=True):
        logging.info(predict_bbox_files)
        if os.path.isfile(predict_bbox_files) and predict_bbox_files.endswith(".txt"): # filter directory
            logging.info(predict_bbox_files)
            new_annot_name = predict_bbox_files.split("/")[-1].split(".")[0] + ".txt"
            processed_annot_file = os.path.join(dest_dir, new_annot_name)
            logging.info(f"Writing to {processed_annot_file}")
            count+=1
            predicted_bbox_dict = process_annotation(predict_bbox_files,
                                                     processed_annot_file,
                                                     )
    logging.info(f"Processed {count} files")
    return None

if __name__ == "__main__":
    # Define log file and logging configuration
    logname = "./errors.log"
    logging.basicConfig(filename = logname,
                        filemode = 'a',
                        format = '%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt = '%H:%M:%S',
                        level = logging.DEBUG)
    # StreamHandler writes to std output
    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

    logging.info("Running main function")

    #Argparser to read in command line inputs
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_folder', help="relative directory containing images file to be infered by model.")
    parser.add_argument('--output_directory', help="relative directory to store bounding box predictions")
    parser.add_argument('--weights',  help="relative path to weights file")
    args = parser.parse_args()

    #Function call
    main()
