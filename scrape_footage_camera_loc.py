from random import randint
from collections import OrderedDict
from datetime import datetime

import logging
import time
import sys
import os
import csv
import argparse
import requests
import schedule


def api_query(args_parsed):
    """Function that makes a query via LTA API for traffic images content and returns the metadata information that is responded.

    Custom request headers is required to prevent the issue of code 429 error encountered as a result of the use of common request headers for queries made by other client through the same API.

    Args:
      url:
        LTA API url to be queried.
      req_headers:
        Request headers for user-agent in python as part of query process

    Returns:
      Dictionary containing the metadata of latest images of traffic condition by traffic cameras if errors are not encountered during request query that was made. None if request related errors are encountered

    Raises:
      None
    """

    req_headers = {"User-agent": args_parsed.agent_id}

    try:
        res = requests.get(args_parsed.lta_api,
                           headers=req_headers,
                           timeout=5)
        # Raise if HTTPError occured
        res.raise_for_status()

        # Check the status code before extending the number of posts
        if res.status_code == 200:
            logging.info("Request sucessful with %s", res.status_code)
            the_json = res.json()
        return the_json['items']

    except requests.exceptions.HTTPError as errh:
        logging.error("Http Error: %s", errh)
    except requests.exceptions.ConnectionError as errc:
        logging.error("Error Connecting: %s", errc)
    except requests.exceptions.Timeout as errt:
        logging.error("Timeout Error: %s", errt)
    except requests.exceptions.RequestException as err:
        logging.error("Exception Error: %s", err)
    return None

def scrape_traffic_image(args_parsed):
    """Main function that extract,process and stores the metadata of the traffic cameras and the image footages returned through the querying of LTA's API for traffic images. It also downloads the traffic footages and organises the images into respective traffic camera ID

    Args:
      args_parsed:
        Parameters passed during script exection.

    Returns:
      None

    Raises:
      IOError: When file could not be accessed.
    """
    logging.info("Scraping image data via api query")
    cctv_feed = api_query(args_parsed)

    number_of_cameras = len(cctv_feed[0]["cameras"])

    for i in range(number_of_cameras):
        logging.info("Processing %s out of %s", i+1,number_of_cameras)
        camera_feed = cctv_feed[0]["cameras"][i]

        # Process information to dictionary
        metadata_dict = {"timestamp" : camera_feed["timestamp"],
              "image_url": camera_feed["image"],
                "lat": camera_feed["location"]["latitude"],
                "lon": camera_feed["location"]["longitude"],
                "camera_id": camera_feed["camera_id"],
                "height": camera_feed["image_metadata"]["height"],
                "width": camera_feed["image_metadata"]["width"],
                "md5": camera_feed["image_metadata"]["md5"]
        }
        metadata_dict = OrderedDict(metadata_dict)
        # Download cctv feed
        download_cctv_feed(args_parsed, metadata_dict)
    return None

def download_cctv_feed(args_parsed, metadata_dict):
    """This function downloads the cctv image feed based on the url information provided as a response from LTA API response.
    Args:
      args_parsed:
        Command line inputs made by users containing model option number and the hyperparameters.
      metadata_dict:
        Ordered dictionary containing various metadata information as returned from LTA API call.
        
    Returns:
      None

    Raises:
      None
    """
    # Timestamp is in the form of yyyy-mm-ddThh:mm:ss+08:00. Convert to yyyymmdd_hhmmss to be used for image name
    rename_timestamp = metadata_dict["timestamp"].replace("-","_").replace(":","").replace("T","_")[:-5]

    # Extract the extension from the url
    extension = metadata_dict["image_url"].split(".")[-1]

    #Create folder based on camera id if required
    folder_name = metadata_dict["camera_id"]
    os.makedirs("./datasets/" + folder_name, exist_ok = True)

    # Define the name of the image to be downloaded
    img_file = "./datasets/" + folder_name + "/"+ rename_timestamp + "." + extension

    metadata_dict.update({"file_name": img_file})
    user_agent_id = args_parsed.agent_id + str(randint(0,500))
    try:
        r = requests.get(metadata_dict["image_url"],
                        stream=True,
                        headers={'User-agent': user_agent_id},
                        timeout=5
                        )

        # Raise if HTTPError occured
        r.raise_for_status()
        # Write to a file if success and log the status
        if r.status_code == 200:
            open(img_file, 'wb').write(r.content)
            logging.info("Successfully downloaded image file %s", metadata_dict["image_url"])

    except requests.exceptions.HTTPError as errh:
        logging.error("Http Error: %s", errh)
    except requests.exceptions.ConnectionError as errc:
        logging.error("Error Connecting: %s", errc)
    except requests.exceptions.Timeout as errt:
        logging.error("Timeout Error: %s", errt)
    except requests.exceptions.RequestException as err:
        logging.error("Exception Error: %s", err)
    return None

def get_cctv_coordinates(args_parsed):
    """Main function that extract,process and stores the metadata of the traffic cameras and the image footages returned through the querying of LTA's API for traffic images. It also downloads the traffic footages and organises the images into respective traffic camera ID

    Args:
      args_parsed:
        Parameters passed during script exection.

    Returns:
      None

    Raises:
      IOError: When file could not be accessed.
    """
    logging.info("Scraping image data via api query")
    cctv_feed = api_query(args_parsed)

    number_of_cameras = len(cctv_feed[0]["cameras"])
    # Metadata extraction for each camera

    try:
        # Open file in append mode and creates if does not exist
        with open(args_parsed.camera_coord_metadata, mode='w',
            encoding='utf-8') as csv_file:
            # Define headers and write content from dictionary
            headers = ['camera_id', 'lat', 'lon']
            writer = csv.DictWriter(csv_file, fieldnames = headers)
            writer.writeheader()
            for i in range(number_of_cameras):
                logging.info("Processing %s out of %s traffic cameras", i+1,number_of_cameras)
                camera_feed = cctv_feed[0]["cameras"][i]

                # Process information to dictionary
                cctv_location_dict = {
                    "camera_id": camera_feed["camera_id"],
                    "lat": camera_feed["location"]["latitude"],
                    "lon": camera_feed["location"]["longitude"],
                }
                writer.writerow(cctv_location_dict)
    except IOError as exc:
        logging.error("I/O error encountered when opening %s", args_parsed.
          camera_coord_metadata)
        raise IOError from exc
    return None


if __name__ == "__main__":

    # Parsers to read arguments passed into this script
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(title='mode',
                                      description='Mode of operation',
                                      help='Either scrape or get_cctv_coordinates',
                                      dest='mode', required=True)

    # First mode of operation: Extract cctv ID and coordinates mapping
    parser_cctv_coordinates = subparser.add_parser('get_cctv_coordinates')

    parser_cctv_coordinates.add_argument('--lta_api', type=str, required=True,
                        help='LTA API link for traffic images.')

    parser_cctv_coordinates.add_argument('--camera_coord_metadata', type=str,
                                         required=True,             help='Relative path to create a camera ID-coordinates mapping file for storage.')
                                         
    parser_cctv_coordinates.add_argument('--agent_id', type=str, required=True,
                        help='Agent ID for use in querying.')

    parser_cctv_coordinates.add_argument('--log_file', type=str, required=True,
                        help='Path where logs are stored.')

    # Second mode of operation: Extract footages
    parser_extract_footage = subparser.add_parser('extract_footage')

    parser_extract_footage.add_argument('--lta_api', type=str, required=True,
                        help='LTA API link for traffic images')

    parser_extract_footage.add_argument('--metadata_file', type=str,
                                         required=True,
                                         help='Relative path to create a file for storing metadata')

    parser_extract_footage.add_argument('--agent_id', type=str, required=True,
                        help='Agent ID for use in querying')

    parser_extract_footage.add_argument('--log_file', type=str, required=True,
                        help='Path where logs are stored')

    parser_extract_footage.add_argument('--end_time', type=str, required=True,
                        help='Ending time to conduct scraping')
    args = parser.parse_args()

    # Define logging configuration
    logging.basicConfig(filename=args.log_file,
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.DEBUG)
    # StreamHandler writes to std output
    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

    # Get cctv coordinates or extract traffic condition footages from cctv
    if args.mode == 'get_cctv_coordinates':
        get_cctv_coordinates(args)

    else:
        end_time = datetime.strptime(args.end_time, "%d/%m/%Y-%H:%M")

        # Run schedule job every 20 seconds, starting 20 seconds from now. This to prevent flooding the API with many request and heuristically images are updated every 20 seconds.
        logging.info('Scheduling query 20 seconds from now till %s', end_time)

        try:
            scraper_job = schedule.every(20).seconds.until(end_time).do(scrape_traffic_image, args)
            
            while True:
                # Run all jobs that are scheduled to run.
                n = schedule.idle_seconds()
                if n is None:
                    # no more jobs
                    logging.info("No scheduled jobs left, terminating...")
                    schedule.clear()
                    break
                else:
                    # sleep exactly the right amount of time before next job
                    logging.info("Sleeping for %s seconds till next job...", n)
                    time.sleep(n)
                    schedule.run_all()
        except schedule.ScheduleValueError:
            logging.error("Unable to schedule job to end at a time in the past. Please check your inputs!!!")