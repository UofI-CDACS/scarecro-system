# Blynk (Legacy SkyWeather Carrier)
This carrier connects weather_rack data to a legacy blynk SkyWeather system. This carrier is very specific to this system. 

## Filename
src/carriers/
- blynk.py

## Dependencies
- python libraries you will need include:
    - sys
    - time
    - requests
    - logging
    - json
  

## Carrier Configuration Info:
- "source": "blynk" 
-  "url": (String or None) the url of the blynk app **Default**: None
-  "blynk_auth": (String or None) the authorization string for the blynk app **Default**: None
-  "units": ("English" or "Metric") The unit system for outputs.  **Default**: "Metric" 
-  "device_ids": (Dict) a dictionary of key (string sensor_name) value (numeric or string sensor id) pairs for identifying a particular sensor to report. **Default**: {} (empty dictionary)

- Example: 
/configs/carriers/:
**blynk_cloud.json**:

        {
            "source": "blynk",
            "blynk_url": "http://blynk.some_url,
            "blynk_auth": "some_auth_string", 
            "units": "English",
            "device_ids": {
                "weather_rack": 20,
                "bmp280": "0",
                "renogy_solar_charger":"renogy_mac",
                "aqi": 1
            }
        }

## Send/Receive and Durations: 
- receive:
    - not supported for this carrier
- send: 
    - "always" duration **is not supported**. 

## Address Configurations: 
- no additional configurations for the address 
    
- Example: 
**blynk_out.json**:
        {
            "inheritance":[],
            "handler": null,
            "handler_function": null,
            "send_or_receive": "send",
            "message_type":  [
                "weather_rack",
                "renogy_solar_charger",
                "bmp280"
            ],
            "carrier": "blynk_cloud",
            "duration": 30
        }


## Other Functionality: 
- No other functionality implemented for this carrier. 

## Behavior: 
- The carrier is very specific for the legacy blynk app configuration of the SkyWeather system and has limited use outside of this. 
    
## Tested 
- outward app functions for weather_rack, renogy_solar_charger, bmp280 tested 


