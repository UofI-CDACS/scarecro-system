# S3 (AWS) Carrier
This carrier can store files given to it to a AWS S3 bucket. 

## Filename
src/carriers/
- s3.py

## Dependencies
- You will need i2c devices enabled on your system  
- Other python libraries you will need include:
    - sys
    - os
    - time
    - logging
    - json
    - boto3 

## Carrier Configuration Info:
- "source": "s3" 
-  "bucket_name": (String or None) the name of the bucket that will be used in S3 storage  **Default**: None 
-  "access_key_id": (String or None) the access key id for the bucket.  **Default**: None
-  "secret_access_key": (String or None) the secret access key to the s3 bucket.  **Default**: None
-  "path": (String) the path (inside generated_data/ of interest)  **Default**: "" 
-  "default_cloud_path" (optional): (String) default cloud path  **Default**: "" 
-  "system_id": (String) the id of the  device (common to keyword substitute the system id).  **Default**: "default" 


- Example: 
/configs/carriers/:
**s3_firmware_ota.json**:

        {
            "source": "s3",
            "bucket_name": "some_firmware_bucket_name",
            "access_key_id": "some_access_key",
            "secret_access_key": "some_secret_access_key,
            "path": "firmware_images",
            "system_id": "$system_id"
        }

- Example: 
/configs/carriers/:
**s3_image.json**:

        {
            "source": "s3",
            "bucket_name": "some_image_bucket_name",
            "access_key_id": "some_access_key",
            "secret_access_key": "some_secret_access_key,
            "path": "camera",
            "system_id": "$system_id"
        }


## Send/Receive and Durations: 
- receive:
    - not defined for this carrier - You CAN download from s3, but that is implemented more as a task than a receive function in the carrier. Unclear whether this is the best implementation or not 
- send: 
    - "always" duration **not supported** for this carrier. All other durations are. 

## Address Configurations: 
- in the "additional_info" section:
    - "sub_path": (String or None) sub path location of the files inside the carrier configured path, if applicable **Default**: None 
    
- Example (upload): 
**s3_upload.json**:

        {
            "inheritance":[],
            "message_type": [
                "image_info"
            ],
            "handler": null,
            "handler_function": null,
            "send_or_receive": "send",
            "carrier": "s3_image",
            "duration": "on_message",
            "additional_info": {
                "sub_path": "$system_id"
            } 
        }




## Other Functionality: 
- - Please see the relevant documentation in the [implemented tasks section here](task_docs/system_maintenance.md)
- Handle New Firmware Task (System Level Task Implemented in this carrier): Uses the handle_new_firmware_message function triggered on message by the "firmware_image" message type to download a new firmware image. This message expects a cloud and disk, as well as a config path and will send a "confirm_receipt" message on success.  

## Behavior: 
- Supresses a lot of the logging from the boto3 library due to the sheer number of messages 
- The path behavior is slightly complex. For the send function:
- the disk path should be in the message as "disk_path". If not, it defaults to the file name
- the cloud path for storage should be in the "cloud_path" key. If not:
    - it will use the s3 path and the address sub path, and the filename to create the new cloud path 
    
## Tested 
- image_info messages to upload images
- firmware_image download


