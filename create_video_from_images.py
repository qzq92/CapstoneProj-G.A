import cv2
import numpy as np
import glob
import logging
import sys
import argparse
import os

def create_video(input_directory,output_directory):
    """
    This function creates a video by using all images within the specified input_directory and saves the create_video
    in the output_directory
    """

    # Extract the cctv_id from the directory path. Assumes it ends with ..../XX
    # where XX refers to the folder representing a specific CCTV ID
    cctv_id = output_directory.split("/")[-1]
    video_name = f"lta_image_video_{cctv_id}.mp4"

    # Declare the a path for glob library which we will iterate through the files inside
    input_folder_directory = os.path.join(input_directory, "**")

    # Declare the location on where to store the video
    output_video_path = os.path.join(output_directory, video_name)

    # Create a list to store the image file names which will be processed when creating the image
    images = []


    for filename in glob.iglob(input_folder_directory, recursive=True):
        if os.path.isfile(filename) and filename.endswith(".jpg"):
            images.append(filename)

    # Sort image name by alphanumeric order
    images.sort()
    # Determine the width and height from the first image and set it as reference since
    # all images from same cctv footage must be of same resolution
    if len(images) > 0:
        logging.info(f"Using {images[0]} as baseline")
        image_path = os.path.join(input_folder_directory, images[0])
        frame = cv2.imread(image_path)
        cv2.imshow('video',frame)
        height, width, channels = frame.shape

        # Define the codec and create VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'mp4v') # Be sure to use lower case
        out = cv2.VideoWriter(output_video_path , fourcc, 3, (width, height))

        logging.info(f"Processing {len(images)} images")

        # Write the images one by one and release the videowriter when it is done.
        for image in images:

            image_path = os.path.join(input_folder_directory, image)
            frame = cv2.imread(image_path)

            out.write(frame) # Write out frame to video

            cv2.imshow('video',frame)
            if (cv2.waitKey(1) & 0xFF) == ord('q'): # Hit `q` to exit
                break

        # Release everything if job is finished
        out.release()
        cv2.destroyAllWindows()

        logging.info(f"The output video is stored in {output_video_path}")
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

    #Parse in arguments from terminal
    #Argparser to read in command line inputs
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_directory', help="directory storing images")
    parser.add_argument('--output_directory', help="place to store dataset directory")
    args = parser.parse_args()

    dataset_dir = os.path.join(os.getcwd(), "LTAdatasets")
    list_of_cctv_id = os.listdir(dataset_dir)
    logging.info(list_of_cctv_id)

    logging.info(f"Preparing to create videos from images for {len(list_of_cctv_id)} CCTV sources")
    counter = 0
    for i in list_of_cctv_id:
        counter += 1
        logging.info(f"Processing {counter} out of {len(list_of_cctv_id)}")
        input_directory = os.path.join(os.getcwd(), args.input_directory, i)
        output_directory = os.path.join(os.getcwd(), args.output_directory, i)

        #Function call
        create_video(input_directory,output_directory)
