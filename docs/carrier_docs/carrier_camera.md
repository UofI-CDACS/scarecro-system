# Camera Carrier
This carrier can take picture from several camera versions
## Filename
src/carriers/
- camera.py

## Dependencies
- You will need your camera enabled on your system and will probably want to test this outside of the driver. If you are using the libcamera, you will need that library installed in your system 
- Other python libraries you will need include:
    - time
    - picamera or picamera2, if using picam (depending on system version)
    - datetime
    - pytz
    - dateutil
    - os 
    - PIL
    - logging
    - sys 

## Carrier Configuration Info:
- "source": "camera" 
-  "id": (String) the id of the camera device (common to keyword substitute the system id).  **Default**: "default" 
- "keep_images": (Number) if you use the cleaning functionality, this is how many images to keep in storage total **Default**: 100

- Example: 
/configs/carriers/:
**camera.json**:

        {
            "source": "camera",
            "id": "$system_id",
            "keep_images": 10
        }


## Send/Receive and Durations: 
- receive:
    - "always" duration only duration **not supported** 
- send: 
    - not currently supported for this carrier 

## Address Configurations: 
- in the "additional_info" section:
    - "folder": (String) the folder (inside of generated_data/) where the pictures will be stored **Default**: "images"
    - "camera_type": ("picamera","pi_hawk_eye", or "libcamera" ) The type of camera in use for the address. **Default**: "default" (won't function)
    
    
- Example (picamera): 
**picamera_in.json**:

        {
            "inheritance":[],
            "handler": null,
            "handler_function": null,
            "send_or_receive": "receive",
            "message_type": "image_info",
            "carrier": "camera",
            "duration": 10,
            "additional_info": {
                "folder": "images",
                "camera_type": "picamera"
            } 
        }

- Example (pi_hawk_eye):
**pi_hawk_eye_in.json**:

        {
            "inheritance":[],
            "handler": null,
            "handler_function": null,
            "send_or_receive": "receive",
            "message_type": "image_info",
            "carrier": "camera",
            "duration": 10,
            "additional_info": {
                "folder": "images",
                "camera_type": "pi_hawk_eye"
            } 
        }

- Example (libcamera):
**libcamera_in.json**:

        {
            "inheritance":[],
            "handler": null,
            "handler_function": null,
            "send_or_receive": "receive",
            "message_type": "image_info",
            "carrier": "camera",
            "duration": 10,
            "additional_info": {
                "folder": "images",
                "camera_type": "libcamera"
            } 
        }


## Other Functionality: 
- - Please see the relevant documentation in the [implemented tasks section here](TODO) 
- Clean Camera (Carrier-Specific Task): this uses the clean_camera_pictures function and the configured keep_images parameter to reduce the number of images in storage to only the keep_image number of most recent images. 

## Behavior: 
- The camera carrier is slightly unique in that takes pictures and both stores them to file and generates an image_info-type reading 
- image info reading: 
    - file_name: {file_date}.jpg (date is in utc)
    - disk_path: save_path/image_name
    - cloud path: images/{id passed in}/image_name (this is used for any potential upstream storage of the image, like to an S3 bucket)
    - time: time in utc
    - camera_type: the type of camera used 
- check the carrier code for default camera parameter settings when taking the picture. One TODO is to make these configurable. 

## Tested 
- picamera with picamera library
- pi_hawk_eye camera with libcamera library 


