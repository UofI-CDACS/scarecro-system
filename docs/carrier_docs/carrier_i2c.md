# i2c Carrier
This carrier can theoretically read from i2c devices -- but it not yet generally well developed. Note reading and parsing at the moment is limited to the bmp280 sensor. 
## Filename
src/carriers/
- i2c.py

## Dependencies
- You will need i2c devices enabled on your system  
- Other python libraries you will need include:
    - i2cdevice
    - struct
    - time
    - past
    - sys
    - datetime 
    - pytz
    - logging

## Carrier Configuration Info:
- "source": "i2c" 
-  "id": (String) the id of the  device (common to keyword substitute the system id).  **Default**: "default" 


- Example: 
/configs/carriers/:
**i2c.json**:

        {
            "source": "i2c",
            "id": "$system_id"
        }


## Send/Receive and Durations: 
- receive:
    - all durations supported. If "always", there will be a 5 miunte (300 second) sleep between readings
- send: 
    - not currently supported for this carrier 

## Address Configurations: 
- in the "additional_info" section:
    - "i2c_address": (Number or None) the address of the i2c device **Default**: None 
    
- Example (bmp280): 
**bmp280_in.json**:

        {
            "inheritance": [],
            "handler": null,
            "handler_function": null,
            "send_or_receive": "receive",
            "message_type": "bmp280",
            "carrier": "i2c",
            "duration": 300,
            "additional_info": {
                "i2c_address": 119
            }
        }



## Other Functionality: 
- No other functionality implemented for this driver at the time. 

## Behavior: 
- Currently only works for bmp280 sensor 
- If receive duration is "always" there is a 5 minute (300 second) sleep between readings 
- This is not a very well formed driver at all, as it is essentially device specific. A TODO is to reformat this driver for other i2c sensors more generally, and break out the bmp280 parsing into its own handler. 

## Tested 
- bmp280 switchdoc raspberry pi SkyWeather hat sensor 


