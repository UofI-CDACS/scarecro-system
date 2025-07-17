# SwitchDoc Sensors Handler
This handler processes messages that come from sensors made by Switchdoc Labs via the 433 MHz radio. 

## Filename
src/handlers/
- switchdoc_sensors.py

## Dependencies
- python libraries you will need include:
    - datetime
    - pytz
    - dateutil
    - logging
  

## Handler Configuration Info:
- "source": "switchdoc_sensors" 

- Example: 
/configs/handlers/:
**switchdoc_handler.json**:

        {
            "source": "switchdoc_sensors"
        }

## Processing Functions 
-  process_switchdoc_sensor_message is the only function used to process data. It uses the message type to determine what processing to run on the message. 

## Carrier Configuration Needs
- no specific needs, but this handler is meant specifically to parse a 433 json packet. 

## Address Configurations: 
- no additional address configuration needs for this handler 


- Example: 
**weather_rack_433_in.json**:

        {
            "inheritance":[],
            "message_type": "weather_rack",
            "handler": "switchdoc_handler",
            "handler_function": "process_switchdoc_sensor_message",
            "send_or_receive": "receive",
            "carrier": "433_listener",
            "duration": "always",
            "additional_info": {
                "string_matches": ["SwitchDoc Labs FT020T AIO"],
                "driver": 146
            } 
        }



## Other Functionality: 
- No other functionality implemented for this carrier. 

## Behavior: 
- envelope overrides the message after parsing it out 

## Tested 
- weather_rack
- aqi 
- thunder_board

