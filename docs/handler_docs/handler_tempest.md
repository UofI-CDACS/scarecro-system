# Tempest Handler
This handler processes messages in particular that come from the [Tempest](https://weatherflow.github.io/Tempest/api/) API. 

## Filename
src/handlers/
- tempest.py

## Dependencies
- python libraries you will need include:
    - datetime
    - pytz
    - dateutil
    - logging
  

## Handler Configuration Info:
- "source": "tempest" 

- Example: 
/configs/handlers/:
**tempest.json**:

    {
        "source": "tempest",
    }

## Processing Functions 
-  process_tempest_message is the only directly used processing function. It takes the message type and list of messages (as is defined for handlers) and uses the message type to decide how to process it. It will add the time of request, the id of the system, break out the forecast lists out of the sub-field (for example, for a variable contained in a "daily"" forecast or "hourly, it will become its own field in the message (with a list of values)). 

## Carrier Configuration Needs
No specific carrier configuration needs, but it will expect it to come in json format from the web API (daily values)

## Address Configurations: 
- no additional address configuration needs for this handler. Just needs the handler and function identified. 
- Example: 
**tempest_station_in.json**:
{
    "inheritance":[],
    "message_type": "tempest_station",
    "handler": "tempest",
    "handler_function": "process_tempest_message",
    "send_or_receive": "receive",
    "carrier": "api_listener",
    "duration": 300,
    "additional_info": {
        "request_type": "GET",
        "url": "https://swd.weatherflow.com/swd/rest/observations/station/<your_station>?token=<your_pat>"
    } 
}


## Other Functionality: 
- No other functionality implemented for this handler. 

## Behavior: 
- This driver will override the system envelope with the parsed content. 
- Please be careful and cognizant of the usage limits for Tempest
- For the forecast, lists of readings are replaces with the forecast_type prefix (day or hour) before the field name, followed by a list of values 

## Tested 
- tempest_station
- tempest_forecast

