# Some Basic System Maintenance Tasks
There are a couple of tasks implemented that perform some basic system duties which are useful to have. These include
- checking the connection status of a system and alerting if the connection has been lost
- clean up the local camera image store
- cleaning up the local databas store 

## Checking the Connection of the System and Alerting if Connection Lost 
### Source Code
/src/tasks/
**system_maintenance.py**

The system_maintenance.py file contains the function which implements the task here.

### Dependencies:
- Python libraries:
    - time
    - os
    - logging
    - sys

### Messages 
- no particular types of messages are needed for this task 


### Default Implementation 
#### Recommended Tasks and Ties to Source Code 

##### check_connection.json 

    {
        "source": "system_maintenance",
        "function": "check_connection",
        "arguments": {},
        "duration": 1200, 
        "alert_emails": ["your_email@email.com"],
        "lost_connection_patience": 2,
        "system_id": "$system_id"
    }

The system_maintenance task class expects the following arguments in the task config:

- "alert_emails": (List of Strings or None), a list of email addresses to alert. **Default**: None
- "lost_connection_patience": (Number): Number of times task has run without connection before altering **Default**: 2
- "system_id": id of the system, likely keyword substituted in, **Default**: "000" 


The check_connection function is meant to run on a numeric duration and does the following:
- checks the system object's connection status
- if the system is disconnect (the number of times above the set patience)
    - it sends an email alert message about the disconnection
    - it attempts to reboot the system 

#### Configurations Needed to Implement in the System:
**Gateway**:

Messages:
- No particular

Carriers:
- mqtt_cloud (or something that monitors its own connection)

Addresses: 
- None in particular - some that relate to the monitored connection 

Task Configs:
- check_connection


**Data Store or Middle Agent**:
- Same as gateway, depends on where implemented 


### Tests 
TODO: Describe these better
- test_reboot_on_disconnection.py 











## Cleaning the Number of Images in the Local Camera Store
### Source Code
/src/carriers/
**camera.py**

The camera.py file contains the function which implements the task here.

### Dependencies:
- Python libraries:
    - time
    - picamera or picamera2, depending on system
    - datetime
    - pytz
    - dateutil
    - os
    - PIL
    - logging
    - sys 

### Messages 
- no particular types of messages are needed for this task 


### Default Implementation 
#### Recommended Tasks and Ties to Source Code 

##### clean_camera.json 

    {
        "source_type": "carrier",
        "config_name": "camera",
        "function": "clean_camera_pictures",
        "arguments": {},
        "duration": 86400
    }


The camera carrier expects, on configuration, a "keep_images" numeric parameter with the total number of images to keep in the store


The clean_camera_pictures function is meant to run on a numeric duration and does the following:
- for every associated address, grab the photo filenames
- sort by recency
- delete images until the desired keep number is reached 

#### Configurations Needed to Implement in the System:
**Gateway**:

Messages:
- No particular

Carriers:
- camera 

Addresses: 
- any time of camera address that takes images 

Task Configs:
- clean_camera


**Data Store or Middle Agent**:
- Same as gateway, depends on where implemented 


### Tests 
TODO: Describe these better
- test_clean_camera.py


## Cleaning the Local Database
### Source Code
/src/carriers/
**mongodb.py**

The mongodb.py file contains the function which implements the task here.

### Dependencies:
- Python libraries:
    - sys
    - pymongo (pi version == 2.4)
    - logging
    - json
    - copy

### Messages 
- no particular types of messages are needed for this task 


### Default Implementation 
#### Recommended Tasks and Ties to Source Code 

##### clean_database.json 

    {
        "source_type": "carrier",
        "config_name": "mongodb_local",
        "function": "clean_database",
        "arguments": {},
        "duration": 86400
    }



The mongodb carrier expects, on configuration, a "retain_days" numeric parameter with the total number of days of data to keep in the database


The clean_database function is meant to run on a numeric duration and does the following:
- if the retain days parameter is set
    - for every collection 
        - delete any record older than now - retain days number

#### Configurations Needed to Implement in the System:
**Gateway**:

Messages:
- No particular

Carriers:
- mongodb_local 

Addresses: 
- any type of mongo address

Task Configs:
- clean_database


**Data Store or Middle Agent**:
- Not really meant for middle agent or main DB 


### Tests 
TODO: Describe these better
- test_mongo_clean.py 