# API Carrier 
This carrier uses the python requests library to ping api endpoints 
## Dependencies
Python libraries you will need include:
    - sys
    - time
    - requests
    - logging
    - json

## Carrier Configuration Info: 
- "source": "api"
- The carrier itself does not need any particular configuration info, as this is implemented on the address level. Only the source: api key is expected. 
- Example: 
/configs/carriers/:
**api_listener.json**:

    {
        "source": "api"
    }

## Send/Receive and Durations: 
- receive:
    - All durations are supported, but if you choose the "always" duration, it will default to sending requests every 5 minutes (300 seconds). This currently can't be configured (TODO: make this configurable)
- send: 
    - not supported by this carrier

## Address Configurations: 
- in the "additional_info" section:
    - "request_type": (string, "GET", or "POST") a list of strings that the incoming json message can match to identify it (**default in carrier**: "GET")
    - "url": (String, or None) the url of the endpoint to ping (**Default**: None) NOTE: This url would include any arguments or authorization tokens, as there is no parsing or combination mechanisms currently implemented in the carrier. If you need more complex behavior, we would recommend making an api-specific carrier for the endpoint(s) you plan to use 
    - "headers" (dict, or None): A dictionary of header names and string values, in the format expected by the python requests dictionary, for the given api (**Default**: None) (POST only)
    - "data": (string, or None): A string of the data to send via the post request (**Default**: None) (POST only)


- Example: 
**open_meteo_daily_in.json**:

    {
        "inheritance":[],
        "message_type": "open_meteo_daily_forecast",
        "handler": "open_meteo_forecasts",
        "handler_function": "process_open_meteo_message",
        "send_or_receive": "receive",
        "carrier": "api_listener",
        "duration": 86400,
        "additional_info": {
            "request_type": "GET",
            "url": "https://api.open-meteo.com/v1/forecast?latitude=47.6825&longitude=-116.796944&daily=weather_code,temperature_2m_max,temperature_2m_min,apparent_temperature_max,apparent_temperature_min,sunrise,sunset,sunshine_duration,daylight_duration,uv_index_max,uv_index_clear_sky_max,rain_sum,showers_sum,snowfall_sum,precipitation_sum,precipitation_hours,precipitation_probability_max,wind_speed_10m_max,wind_direction_10m_dominant,wind_gusts_10m_max,shortwave_radiation_sum,et0_fao_evapotranspiration,wet_bulb_temperature_2m_mean,wet_bulb_temperature_2m_max,wet_bulb_temperature_2m_min,vapour_pressure_deficit_max,surface_pressure_mean,surface_pressure_max,surface_pressure_min,updraft_max,visibility_mean,visibility_min,visibility_max,winddirection_10m_dominant,wind_gusts_10m_mean,wind_speed_10m_mean,wind_gusts_10m_min,wind_speed_10m_min,et0_fao_evapotranspiration_sum,leaf_wetness_probability_mean,precipitation_probability_mean,precipitation_probability_min,growing_degree_days_base_0_limit_50,relative_humidity_2m_mean,relative_humidity_2m_max,relative_humidity_2m_min,temperature_2m_mean,apparent_temperature_mean,cape_mean,cape_max,cape_min,cloud_cover_mean,cloud_cover_max,cloud_cover_min,dew_point_2m_mean,dew_point_2m_max,dew_point_2m_min,snowfall_water_equivalent_sum,pressure_msl_mean,pressure_msl_max,pressure_msl_min&timezone=GMT&wind_speed_unit=mph&temperature_unit=fahrenheit"
        } 
    }

This uses the open-meteo url and handler to get (once a day) a 7-day forecast on a variety of weather variables. 

## Other Functionality: 
- No other tasks or standalone functionality is implemented for this carrier. 


## Behavior: 
- It is likely each endpoint will need its own handler, as data returned from endpoints can vary widely 


## Tested Sensors
- Open-Meteo daily
