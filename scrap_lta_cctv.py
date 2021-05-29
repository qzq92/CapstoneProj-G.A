import schedule
import time
import requests
import os
import sys
import csv
from random import randint
from os.path import splitext
from collections import OrderedDict
import logging

def api_query(url = "https://api.data.gov.sg/v1/transport/traffic-images", req_headers = {"User-agent": "Capstone_QZQ"}):
    """
    Function that takes in url and number of queries which are used in determining the amount of queries
    to be made from a site url for the purpose of collecting LTA posts. An additional request header
    was required to prevent the issue of code 429 error caused by the use of common request header by various
    client end points on the same page.

    Arguments:
    @url: defaults to lta api url to be queried
    @req_headers: Customised user agent for python
    """
    #posts = []

    res = requests.get(url, headers = req_headers)
    # Check the status code before extending the number of posts
    if res.status_code == 200:
        logging.info("Request sucessful with {res.status_code}")
        the_json = res.json()
        #posts.extend(the_json)
    else:
        logging.log(f"Request failure with {res.status_code}")

    return the_json['items']

def scrape_traffic_image():
    logging.info("Scraping image data...")
    cctv_feed = api_query()

    print(cctv_feed)
    number_of_cameras = len(cctv_feed[0]["cameras"])
    # Metadata extraction for each cameras
    for i in range(number_of_cameras):
        logging.info(f"Processing {i+1} out of {number_of_cameras}")
        camera_feed = cctv_feed[0]["cameras"][i]

        # Convert to dictionary
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

        download_cctv_feed(metadata_dict["image_url"], metadata_dict["timestamp"], metadata_dict)

        #Write information to a csv file
        file_exists = os.path.isfile("./datasets/metadata.csv")
        try:
            # Open file in append mode
            with open("./datasets/metadata.csv", "a") as csv_file:
                # Define headers
                headers = ['timestamp', 'image_url', 'file_name', 'lon', 'lat', 'camera_id','height','width','md5']
                writer = csv.DictWriter(csv_file, fieldnames = headers)
                if not file_exists:
                    writer.writeheader()  # file doesn't exist yet, write a header

                writer.writerow(metadata_dict)
        except IOError:
            logging.info("I/O error")

def download_cctv_feed(image_url, timestamp , metadata_dict):
    #Timestamp is in the form of yyyy-mm-ddThh:mm:ss+08:00. Convert to yyyymmdd_hhmmss to be used for image name
    rename_timestamp = timestamp.replace("-","_").replace(":","").replace("T","_")[:-5]
    print(rename_timestamp)

    #Extract the extension from the url
    extension = image_url.split(".")[-1]

    #Create folder based on camera id
    folder_name = metadata_dict["camera_id"]
    os.makedirs("./datasets/" + folder_name, exist_ok = True)

    # Define the name of the image to be downloaded
    img_file = "./datasets/" + folder_name + "/"+ rename_timestamp + "." + extension
    metadata_dict.update({"file_name": img_file})
    user_agent_id = 'LTA_Scrape_QZQ' + str(randint(0,500))
    r = requests.get(image_url,
                    stream = True,
                    headers = {'User-agent': user_agent_id})
    if r.status_code == 200:
        # Write to a file if success
        open(img_file, 'wb').write(r.content)
        logging.info(f"Successfully downloaded image file {image_url}")
    else:
        logging.info(f"Unable to download image file {image_url}")
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
    # Run job every 20 second, starting 3 second/minute/hour/day/week from now
    schedule.every(20).seconds.do(scrape_traffic_image)
    while True:
        logging.info("Starting scheduler")
        schedule.run_pending()
        logging.info("Sleeping for 60 seconds")
        time.sleep(60)
