# Recovering Data from the Local SCARECRO Store on Connection Outage (Getting Data Logger Info Back)
On occasion, a piece of the system might lose connectivity with the other parts of the system. If local storage is configured, this data should be able to be recovered by the system. 

This document aims to outline the implemented process used for SCARECRO to recovery data. There are different potential ways to recover data, including a **push** stragety (entity recognizes it's lack of connectivity) or a **pull** strategy (separate entity recognizes different entity's lack of connectivity). For simplicity, this implementation will use a **push** strategy, having gateways recognize their own lack of connectivity before sending up the missing data. 

## Source Code
The recovery.py file contains the recovery python class which implements the functionality here. 

## Messages 
This system works by sending several types of messages. These are: 
* connection_status
* recovery_data_request
* recovery_data

## connection message 
Should look like: 

    {
        "connection_status": "disconnect", (or "reconnect")
        "time": time_of_lost_connection, 
        "id": (optional, name of thing that noticed)
    }

## recovery_data_request message
Should look like:

    {
        "id": system_id
        "time": time of message
        "lost_connection_time": time connection was lost
        "restored_connection_time": time connection was restored 
    }

## recovery_data message
Should look like:

    {
        "id": system_id
        "entity": (optional) - entity that recovered data
        "lost_connection_time": time connection was lost
        "restored_connection_time": time connection was restored
        "recovery_data": {
            message_type: [list of entries],
            message_type: [list of entries],
        }

    }

## Recommended Flow for General Implementation
The flow for the system should work as follows: 

1. Some part of the gateway (or multiple potential parts) notice that the gateway has lost connection to the internet or main channel of communication. This entity posts a connection_status message noting the disconnect. 

2. The connection_status message should have an on_message trigger that indicates a recovery task function. If a disconnection has not already been noticed, the time of lost connection should be stored to non-volatile storage. An internal system variable should also be tracking whether or not the gateway is connected. 

3. At some point later (or on system startup, as the case may be), the parts of the gateway or (multiple potential parts) should notice that the connection has been restored. This entity posts a connection_status message noting the restored connection. 

4. The restored connection_status message should have an on_message trigger to a recovery task function. This should change the system variable to connected, and decide whether or not the outage was long enough to justify recovering data. If it was, the system should generate a recovery_data_request message. 

5. The recovery_data_request should have an on_message trigger which going to the data store function, which grabs the requested data of interest for the time period of interest. It then posts a recovery data message. (It may be a good idea to break these into multiple recovery data messages if the size is too large)

6. The recovery_data message should have an on_message trigger going to the middle agent or final data store. 

7. The recovery_data message should have an inbound on_message trigger going to the data store. This should store data, potentially check for duplicates, and add the "source": "recovery" field or something similar.  




## Default Implementation 
### Recommended Tasks and Ties to Source Code 

#### handle_connection_change task 

    {
        "source": "recovery",
        "function": "handle_connection_message",
        "arguments": {},
        "duration": "on_message",
        "message_type": "connection_status" 
    }

When some communication entity (in most of our setups, we use the MQTT carrier) notices it has lost a connection allowing it to submit upstream data, it generates a connection_status message. This triggers the "handle_connection_message" function of the recovery object (in the tasks source code file). This function: 
- picks up the message(s)
- checks each to see if it's a disconnect or a reconnect. 
- if it is a disconnect: 
    - sets the **system** disconnection variable to True 
    - generates a disconnect connection status (for writing to file - includes the connection status and date/time)
    - sets its **internal** object connection variable to False
    - gets the file (stored in generated_files/connection_info.json)
    - If the file does not already have a disconnect written, it writes the disconnection to the file (this way it persists across a reboot)
- if it is a reconnect: 
    - sets the **system** disconnection variable to True
    - generates a reconnect connection status (for writing to file - includes the connection status and date/time)
    - sets its **internal** object connection variable to True
    - gets the file (stored in generated_files/connection_info.json)
    - If the file does not already have a reconnect written:
        - it writes the reconnect to the file (this way it persists across a reboot)
        - it generates a request for recovery data (to recover any data lost during the outage period) (recovery_data_request)
            - this function looks at the lost and restored connection time and posts a recovery data message request if both lost and restored connection times are valid 

#### handle_request_for_recovery_data task

    {
        "source_type": "carrier",
        "config_name": "mongodb_local",
        "function": "fetch_recovery_data",
        "arguments": {},
        "duration": "on_message",
        "message_type": "recovery_data_request" 
    }


The local database connection (in our case, mongodb) handles this recovery data request message trigger. The "fetch_recovery_data" function of our database carrier is called. This function: 
- picks up the message(s) 
- gets the lost and restored connection time from the messages 
- for all of its relevant collections:
    - it gets all records in the time range of interest (it adds the source: "recovery" key/value during this step, so you know the reading was recovered)
    - if there are records, it adds the records to a dictionary (key = collection, value = entries as a list)
- envelopes and posts a recovery data message 

#### handle_recovery_data task 

    {
        "source_type": "carrier",
        "config_name": "mongodb_cloud",
        "function": "handle_recovery_data_message",
        "arguments": {},
        "duration": "on_message",
        "message_type": "recovery_data" 
    }

This tasks is trigged on a recovery_data message, and is handled by the handle_recovery_data_message of the main/remote data store (cloud MongoDB in our case). This function does the following: 
- picks up the message(s)
- gets the lost/restored connection times and the recovery data 
- for each message type, tries to eliminate duplicate entries already in the database (takes a few database calls)
- if there are still entries after eliminating duplicates, it adds them to the database 


### Configurations Needed to Implement in the System:
**Gateway**:

Messages:
- connection_status (noted in task config)
- fetch_recovery_data (noted in task config)
- recovery_data (for outbound sending) - noted in address 

Carriers:
- mongodb_local (noted in task config)

Addresses: 
- cloud_mqtt_send_immediate (for outbound to middle agent/data store) - recovery data message

Task Configs:
- handle_connection_change,
- handle_request_for_recovery_data


**Data Store or Middle Agent**:

Messages:
- recovery_data (noted in task config) (for inbound receipt)

Carriers:
- mongodb_cloud (for obtaining recovery data)

Addresses: 
- cloud_mqtt_receive (to receive recovery data message)
- mongo_cloud_immediate (for recovery data insertion)

Tasks:
- handle_recovery_data


## Tests 
TODO: Describe these better
- test_disconnect_message
- test_disconnect_recognition_mqtt 
- test_reboot_on_disconnection 
- test_recovery_eliminate_duplicates_offline 
- test_recovery_gateway 
- test_recovery_retrieval
- test_recovery_middle_agent 
- test_recovery_retrieval_middle_agent 


## Limitations
- No system-wide feedback currently implemented on DB side of whether recovery data was successfully added 

