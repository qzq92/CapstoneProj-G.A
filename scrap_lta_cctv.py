from random import randint
from collections import OrderedDict
from datetime import datetime

import schedule
import time
import requests
import os
import sys
import csv
import argparse
import logging


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
            logging.info("Request sucessful with {res.status_code}")
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
    # Metadata extraction for each camera
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

        # Write information to a csv file
        try:
            # Open file in append mode and creates if does not exist
            with open(args_parsed.metadata_file, mode='a+', encoding='utf-8') as csv_file:
                # Define headers and write
                headers = ['timestamp', 'image_url', 'file_name', 'lon', 'lat', 'camera_id','height','width','md5']
                writer = csv.DictWriter(csv_file, fieldnames = headers)
                writer.writerow(metadata_dict)
        except IOError as exc:
            logging.error("I/O error encountered when opening %s", args_parsed.metadata_file)
            raise IOError from exc
    return None

def download_cctv_feed(args_parsed, metadata_dict):
    """This function downloads the cctv image feed based on the url information provided as a response from LTA API response.
    Args:
      args_parsed:
        Command line inputs made by users containing model option number and the hyperparameters.
      metadata_dict:
        
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

if __name__ == "__main__":

    # Parsers to read arguments passed into this script
    parser = argparse.ArgumentParser()
    parser.add_argument('--lta_api', type=str, required=True,
                        help='LTA API link for traffic images')
    parser.add_argument('--metadata_file', type=str, required=True,
                        help='Relative path to create a file for storing metadata')
    parser.add_argument('--agent_id', type=str, required=True,
                        help='Agent ID for use in querying')
    parser.add_argument('--log_file', type=str, required=True,
                        help='Path where logs are stored')
    parser.add_argument('--end_time', type=str, required=True,
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

    # Parsers to read arguments passed into this script
    parser = argparse.ArgumentParser()
    parser.add_argument('--lta_api', type=str, required=True,
                        help='LTA API link for traffic images')
    parser.add_argument('--metadata_file', type=str, required=True,
                        help='Relative path to create a file for storing metadata')
    parser.add_argument('--agent_id', type=str, required=True,
                        help='Agent ID for use in querying')
    parser.add_argument('--end_time', type=str, required=False,
                        help='Ending time to conduct scraping')
    args = parser.parse_args()

    # Run job every 20 second, starting 3 second/minute/hour/day/week from now
    schedule.every(20).seconds.do(scrape_traffic_image, args)

    current_time = datetime.now()
    end_time = datetime.strptime(args.end_time, "%d/%m/%Y %H:%M")
    while current_time <= end_time:
        logging.info("Starting scheduler")
        schedule.run_pending()
        
        logging.info("Sleeping for 60 seconds")
        time.sleep(60)
