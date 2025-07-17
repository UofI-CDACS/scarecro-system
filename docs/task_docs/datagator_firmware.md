# Downloading a New Data Gator Firmware Image to Local Storage
If you have a system configured with a SCARECRO gateway that communicates to a Data Gator device, it is useful to be able to run over-the-air (OTA) updates to the Data Gator firmware. To facilitate this, there is a special folder inside of the raspberry pi where firmware images are stored and can be pinged by the Data Gator. This document describes the implementation of OTA Data Gator firmware for a gateway. 

## Source Code
/src/carriers/
**s3.py**

The s3.py file contains the function which implements the task here.

## Dependencies:
- Python libraries:
    - sys
    - os
    - time
    - logging
    - json
    - boto3 

## Messages 
- firmware_image 
- confirm_receipt

## firmware_image message 
Should look like: 

    {
        "id": id of sender,
        "time": time of send,
        "file_name": name of the firmware image to get
        "cloud_path": location of the file in the cloud (includes filename)
        "disk_path": where to write the firmware image (includes filename)
        "config_path": file to write the new firmware image name to, locally (includes filename)
        "confirm_receipt": (True/False), whether to send a "confirm receipt" message after download
    } 

## confirm_receipt message

    {
        "id": system id
        "file_name": file_name,
        "confirm_receipt": True,
        "time": time of receipt
    }

## Recommended Flow for General Implementation
The flow for the get new firmware task should work as follows. 

1. A new firmware version for the data gator is written. When it is published, a "firmware_image" message is sent out to the system. 

2. The part of the system that has access to the firmware image store downloads the new image, and writes the new file name to a config. 

## Default Implementation 
### Recommended Tasks and Ties to Source Code 

#### download_new_firmware_image.json 

    {
        "source_type": "carrier",
        "config_name": "s3_firmware_ota",
        "function": "handle_new_firmware_message",
        "arguments": {},
        "duration": "on_message",
        "message_type": "firmware_image" 
    }


When a firmware_image messages comes in, the s3 carrier runs the handle_new_firmware_image function. This function: 
- gets the cloud and disk paths
- downloads the file
- updates the firmware config file 
- posts a confirm_receipt message, if the system asks it to. 


### Configurations Needed to Implement in the System:
**Gateway**:

Messages:
-  firmware_image (noted in task config)
- confirm_receipt 

Carriers:
- s3_firmware_ota (noted in task config)

Addresses: 
- cloud_mqtt_receive (for incoming firmware_imagea message
- cloud_mqtt_send_immediate (for outbound confirm_receipt message, possible)

Task Configs:
- download_new_firmware_image


**Data Store or Middle Agent**:
- Same as gateway, depends on where implemented 


## Tests 
TODO: Describe these better
- test_ota_firmware_download