# Mongodb Carrier
This carrier uses sends and pulls messages from a mongodb database (local or cloud). It also makes use of recovery and update tasks via its interface. 

## Filename
src/carriers/
- mongodb.py

## Dependencies
- If you are planning to use a local mongodb on your system, you would need that installed. For a cloud mongodb, you would just need connection info. 
TODO: Link [Check out the installation instructions for the library here]()
- Other python libraries you will need include:
    - sys
    - logging
    - json
    - copy
    - pymongo
        - on a raspberry pi, with the legacy supported local mongo, you need pymongo version 2.4 to interface with it. 

## Carrier Configuration Info: 
- "source": "mongodb"
- "connection url": (String) the url of the mongo cluster you will be connecting to. **Default**: "127.0.0.1:27017" (the local mongodb default connection)
- "version": (Number) the version of mongodb you will use. **Default**: 4.0
- "database_name": (String or None) the name of the database you will be connecting to. **Default**: None
- "persistent_conenction": (True/False) whether or not will be using a persistent connection with the database. **Default**: True
- "retain_days": (Number or False) the number of days you want to retain data in the database if you are use a clean database task. **Default**: False  

- Example (Local): 
/configs/carriers/:
**mongodb_local.json**:

        {
            "source": "mongodb",
            "connection_url": "127.0.0.1",
            "database_name": "SCARECRO",
            "version": 2.4, 
            "persistent_connection": true,
            "retain_days": 30
        }

- Example (Cloud): 
/configs/carriers/:
**mongodb_cloud.json**:

        {
            "source": "mongodb",
            "connection_url": "your_srv_url",
            "database_name": "SCARECRO",
            "version": 4.0, 
            "persistent_connection": true
        }

## Send/Receive and Durations: 
- receive:
    - not supported for this carrier
- send: 
    - "always" duration **is not supported**
    - durations which **return** (numeric seconds, on_message, as_needed) **are supported**

## Address Configurations: 
- in the "additional_info" section:
    - "collection": (String or None) the name of the collection the message should be stored in inside of the database. **Default**: None
    - "eliminate_duplicates": (Number or None, optional). If this is set to a number, and there is a need to eliminate an incoming message (on the recovery task in particular) it will look for duplicates already in the database for the given sensor instance within the set number of seconds and only insert the record if there is no record within that range. **Default**: None 

- Example: 
**mongo_local_immediate.json**:

        {
            "inheritance":[],
            "message_type": [
                "gateway_stats",
            ],
            "handler": null,
            "handler_function": null,
            "send_or_receive": "send",
            "carrier": "mongodb_local",
            "duration": "on_message",
            "additional_info": {
                "collection": "$msg_type"
            } 
        }

- Example:
**mongo_cloud_immediate.json**:

        {
            "inheritance":[],
            "message_type": [
                "gateway_stats",
            ],
            "handler": null,
            "handler_function": null,
            "send_or_receive": "send",
            "carrier": "mongodb_cloud",
            "duration": "on_message",
            "additional_info": {
                "collection": "$msg_type",
                "eliminate_duplicates": 300
            } 
        }


## Other Functionality: 
- Please see the relevant documentation in the [implemented tasks section here](task_docs/system_maintenance.md)
- Updater Task (System type Task, implemented in this carrier): [See the documentation for the updater class here](../task_docs/updater_class.md). This driver implements the task of fetching updates to configuration via the fetch_configurations function, which can be configured as a task triggered by the "remote_config_updated" message type. This function fetches the new configurations and then posts a "fetched_config" message when finished. 
- Recovery Task (System type task, implemented in this carrier): [See the documentation for the recovery class here](../task_docs/recovery.md). This uses:
    - the fetch_recovery_data function (triggered on a recovery_data_request message) to get recovery data from the database within a certain time range. It adds a recovery source key to recors in the range as well, and then posts a recovery_data message. 
    - the handle_recovery_data_message function (triggered on a recovery data message) which grabs the recovery data, eliminates duplicate messages if already in the database for those configured to use that features, and inserts the new entries
    - note that the flow of this information is usually from a local mongo gateway driver to send the recovery data to the cloud mongo driver to recieve the recovery data and possibly eliminate duplicates.  
- Clean Database Task (Carrier Specific Task): task that takes no arguments but deletes all records for relevant collections before a configured (using retain_days) number of days old. 

## Behavior: 
- Sent Entries: MongoDB driver will only sent messages it has not sent before for a given sensor instance, using the sent_entries variable. 
- Reconnection. If there is an error getting the mongodb collection, inserting records, obtaining records, getting all records in a time range, get a configuration, or deleting records during a clean, the carrier will attempt to reconnect to the database. 
- Persistent Connection: If persistent connection is set, the carrier will connect to the database on initialization. Otherwise, it will connect and disconnect during each isnert operation: TODO: check this behavior on other operations than insert! 
- Timestamps: The carrier converts the timestamps (on database insert) to a more mongo-friendly binary format and converts them back on database pull.  

## Tested 
- Local MongoDB instance on raspberry pi 3B+
- MongoDB Atlas Cluster

