# 433_radio Carrier 
This carrier uses an SDR (tested with a soapy SDR USB plugin) and the rtl_433 library to receive json packets on 433 MHz. 
## Dependencies
- rtl_433 library (switchdoc labs branch). This project uses the rtl_433 library, in particular the switchdoc labs branch (as SCARECRO developed out of the original SkyWeather System from Swithdoc). You will need to have this library installed on the computer you plan to use for this carrier. 

TODO: Link [Check out the installation instructions for the library here]()
- Other python libraries you will need include:
    - sys
    - logging
    - json
    - threading
    - time
    - subprocess
    - Queue or queue 

## Carrier Configuration Info: 
- "source": "433_radio"
- The carrier itself does not need any particular configuration info, as this is implemented on the address level. Only the source: 433_radio key is expected. 
- Example: 
/configs/carriers/:
**433_listener.json**:

    {
        "source": "433_radio"
    }

## Send/Receive and Durations: 
- receive:
    - duration "always" is **supported**
    - other durations are supported and will default to **50 seconds of listening time on the airwaves. If you run this receive function more often, you will likely run into issues**. TODO: Make this configurable with a default. 
- send: 
    - not supported by this carrier

## Address Configurations: 
- in the "additional_info" section:
    - "string_matches": (list of strings) a list of strings that the incoming json message can match to identify it (default in carrier: **[]**)
    - "driver": (Number) the value of the specific 433 driver for the message (default in carrier: **None**) 

- Example: 
**switchdoc_sensors_in.json**:

    {
        "inheritance":[],
        "handler": "switchdoc_handler",
        "handler_function": "process_switchdoc_sensor_message",
        "send_or_receive": "receive",
        "carrier": "433_listener",
        "duration": "always"
    }

**weather_rack_433_in.json**:

    {
        "inheritance":["switchdoc_sensors_in"],
        "message_type": "weather_rack",
        "additional_info": {
            "string_matches": ["SwitchDoc Labs FT020T AIO"],
            "driver": 146
        } 
    }

## Other Functionality: 
- No other tasks or standalone functionality is implemented for this carrier. 
## Behavior: 
- If the carrier notices it has been more than 12 minutes (720 seconds) since it's last receipt of a message, the SDR thread will try and restart itself. You will get a message about killing and restarting the SDR thread. 
## Tested Sensors
- switchdoc labs weather_rack
- swtichdoc labs aqi sensor
- switchdoc labs thunderboard 
