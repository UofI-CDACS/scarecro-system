# Open-Meteo Forecast Handler
This handler processes messages in particular that come from the [Open-Meteo](https://open-meteo.com/) forecast API. 

## Filename
src/handlers/
- open_meteo.py

## Dependencies
- python libraries you will need include:
    - datetime
    - pytz
    - dateutil
    - logging
  

## Handler Configuration Info:
- "source": "open_meteo" 
- "system_id": id of system, likely keyword-substituted 

- Example: 
/configs/handlers/:
**open_meteo_forecasts.json**:

    {
        "source": "open_meteo",
        "system_id": "$system_id"    
    }

## Processing Functions 
-  process_open_meteo_message is the only directly used processing function. It takes the message type and list of messages (as is defined for handlers) and uses the message type to decide how to process it. It will add the time of request, the id of the system, break out the forecast lists out of the sub-field (for example, for a variable contained in "daily", it will become its own field in the message). 

## Carrier Configuration Needs
No specific carrier configuration needs, but it will expect it to come in json format from the web API (daily values)

## Address Configurations: 
- no additional address configuration needs for this handler. Just needs the handler and function identified. 
- Example: (lat and long coordinates are for Coeur d'Alene, Idaho)
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

This uses the lat/long of CDA to get the daily forecast weather data. 

## Other Functionality: 
- No other functionality implemented for this handler. 

## Behavior: 
- The handler will replace the id of the message with the system id. It will add a time of request to the "time" field and attempt to capture forecast time endpoints. It will break out observations into their own fields as defined in the message. 
- This driver will override the system envelope with the parsed content. 
- Please be careful and cognizant of the usage limits for Open-Meteo. 

## Tested 
- open_meteo_daily_forecast 
- open_meteo_current
- TODO: Hourly (Hourly Data includes some soil properties, which would potentially be good to have/forecast)
