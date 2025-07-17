# Underlying System Carrier
This carrier gives information on the scarecro-implementing system itself 

## Filename
src/carriers/
- underlying_system.py

## Dependencies
- python libraries you will need include:
    - datetime
    - pytz
    - psutil
    - re
    - subprocess
    - time
    - logging
    - sys 
    - socket 

## Carrier Configuration Info:
- "source": "underlying_system" 
-  "id": (String) the id of the  device (common to keyword substitute the system id).  **Default**: "default" 


- Example: 
/configs/carriers/:
**underlying_system.json**:

        {
            "source": "underlying_system",
            "id": "$system_id"
        }

## Send/Receive and Durations: 
- receive:
    - all durations supported. If "always", there is a 5 minute sleep between readings. 
- send: 
    - not supported for this carrier

## Address Configurations: 
- in the "additional_info" section:
    - "function": (String) name of the function implementing the message generation.  **No Default**
    
- Example: 
**gateway_stats_in.json**:

        {
            "inheritance":[],
            "handler": null,
            "handler_function": null,
            "send_or_receive": "receive",
            "message_type": "gateway_stats",
            "carrier": "underlying_system",
            "duration": 300,
            "additional_info": {
                "function": "status_reading"
            } 
        }


## Other Functionality: 
- No other functionality implemented for this carrier. 

## Behavior: 
- The carrier is currently using the passed in function name to decide behavior, which is directly coupled with the system reading. This might need to be more generalized. 
- TODO: might be good to get information not just related to system hardware/networking, but also SCARECRO operation performance logs 
    
## Tested 
- gateway_stats messaging


