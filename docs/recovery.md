# Recovery 
On occasion, a piece of the system might lose connectivity with the other parts of the system. If local storage is configured, this data should be able to be recovered by the system. 

This document aims to outline the implemented process used for SCARECRO to recovery data. There are different potential ways to recover data, including a push stragety (entity recognizes it's lack of connectivity) or a pull strategy (separate entity recognizes different entity's lack of connectivity). For simplicity, this implementation will use a push strategy, having gateways recognize their own lack of connectivity before sending up the missing data. 

## Messages 
This system works by sending several types of messages. These are: 

(Could maybe combine lost and restored connection into one message? Not sure)
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

## Flow
The flow for the system works as follows: 

1. Some part of the gateway (or multiple potential parts) notice that the gateway has lost connection to the internet or main channel of communication. This entity posts a lost_connection message. 

2. The lost_connection message should have an on_message trigger that indicates a recovery task function. If a disconnection has not already been noticed, the time of lost connection should be stored to non-volatile storage. An internal system variable should also be tracking whether or not the gateway is connected. 

3. At some point later (or on system startup, as the case may be), the parts of the gateway or (multiple potential parts) should notice that the connection has been restored. This entity posts a restored_connection message. 

4. The restored_connection message should have an on_message trigger to a recovery task function. This should change the system variable to connected, and decide whether or not the outage was long enough to justify recovering data. If it was, the system should generate a recovery_data_request message. 

5. The recovery_data_request should have an on_message trigger which going to the data store function, which grabs the requested data of interested for the time period of interest. It then posts a recovery data message. (May break these into multiple recovery data messages if too large)

6. The recovery_data message should have an on_message trigger going to MQTT out to the middle agent

7. The recovery_data message should have an inbound on_message trigger going to the data store. This should store data, potentially check for duplicates, and add the "source": "recovery" field or something similar.  


