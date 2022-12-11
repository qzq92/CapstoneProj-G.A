#!/bin/bash

# Configurations for querying traffic images from LTA API to datamall.

# LTA API URL
LTA_API_URL=https://api.data.gov.sg/v1/transport/traffic-images

# Path to create file for storing of whole metadata info of traffic cameras returned by API
METADATA_FILE=metadata.csv

# Path to store traffic camera ID to coordinates mapping
CAMERA_COORD_FILE=camera_coordinates.csv

# Request head for user-agent to be used when conducting API query. Like identifier
AGENT_ID=Capstone_QZQ

# Logfile path
LOG_FILE=errors.log

# Endtime to stop scraping (dd/mm/yyyy-hh:mm format)
END_TIME=11/12/2022-21:37

# Extracting traffic camera IDs and coordinates mappings. Comment out either of the following code blocks if you do not intend to run the specific operations.
#echo "Extracting traffic camera IDs and coordinates mapping."
#echo " "
#python scrape_footage_camera_loc.py get_cctv_coordinates --lta_api $LTA_API_URL --camera_coord_metadata $CAMERA_COORD_FILE --agent_id $AGENT_ID --log_file $LOG_FILE 

# Scraping of traffic footages periodically till specified end time. Comment out either of the following code blocks if you do not intend to use any of the model.
 echo "Scraping traffic footages via LTA API URL..."
 echo " "
 python scrape_footage_camera_loc.py extract_footage --lta_api $LTA_API_URL --metadata_file $METADATA_FILE --agent_id $AGENT_ID --log_file $LOG_FILE --end_time $END_TIME

echo "Exiting program."
exit 0