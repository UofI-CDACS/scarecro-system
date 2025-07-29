from datetime import datetime, timedelta, tzinfo
from datetime import timezone
from datetime import date
import pytz
from dateutil import tz 
import logging 


class OpenMeteo:
    """
    This class makes use of the Open-Meteo Weather data from their 
    API documented here: https://open-meteo.com/
    """
    def __init__(self, config={}, send_addresses={}, receive_addresses={}, message_configs={}):
        #These are optional - if your program needs them 
        """
        Takes in: a configuration dictionary for this handler,
        A dictionary of addresses for the handler for sending, (dictionary?)
        A dictionary of addresses for the handler for receiving (dictionary?), 
        A dictionary of message definitions indicated in the addresses 
        """
        self.config = config.copy()
        self.send_addresses = send_addresses.copy()
        self.receive_addresses = receive_addresses.copy()
        self.message_definitions = message_configs.copy()
        #Debug Step 
        logging.info("Initing Open Meteo Forecast handler")
        #Put in the system id 
        self.system_id = self.config.get("system_id", "default")
    

    def envelope_id_override(self, message_envelope, message_content): 
        message_def = self.message_definitions.get(message_envelope.get("msg_type", None), {})
        message_envelope["msg_content"] = message_content
        message_envelope["msg_id"] = message_content.get(message_def.get("id_field", "id"), "default")
        message_envelope["msg_time"] = message_content.get(message_def.get("time_field", "time"), "default")
        return message_envelope


    def parse_daily(self, message):
        """
        Using JSON message format returned from this link:
        #https://api.open-meteo.com/v1/forecast?latitude=47.6825&longitude=-116.796944&daily=weather_code,temperature_2m_max,temperature_2m_min,apparent_temperature_max,apparent_temperature_min,sunrise,sunset,sunshine_duration,daylight_duration,uv_index_max,uv_index_clear_sky_max,rain_sum,showers_sum,snowfall_sum,precipitation_sum,precipitation_hours,precipitation_probability_max,wind_speed_10m_max,wind_direction_10m_dominant,wind_gusts_10m_max,shortwave_radiation_sum,et0_fao_evapotranspiration,wet_bulb_temperature_2m_mean,wet_bulb_temperature_2m_max,wet_bulb_temperature_2m_min,vapour_pressure_deficit_max,surface_pressure_mean,surface_pressure_max,surface_pressure_min,updraft_max,visibility_mean,visibility_min,visibility_max,winddirection_10m_dominant,wind_gusts_10m_mean,wind_speed_10m_mean,wind_gusts_10m_min,wind_speed_10m_min,et0_fao_evapotranspiration_sum,leaf_wetness_probability_mean,precipitation_probability_mean,precipitation_probability_min,growing_degree_days_base_0_limit_50,relative_humidity_2m_mean,relative_humidity_2m_max,relative_humidity_2m_min,temperature_2m_mean,apparent_temperature_mean,cape_mean,cape_max,cape_min,cloud_cover_mean,cloud_cover_max,cloud_cover_min,dew_point_2m_mean,dew_point_2m_max,dew_point_2m_min,snowfall_water_equivalent_sum,pressure_msl_mean,pressure_msl_max,pressure_msl_min&timezone=GMT&wind_speed_unit=mph&temperature_unit=fahrenheit
        #https://api.open-meteo.com/v1/forecast?latitude=47.6825&longitude=-116.796944&daily=weather_code,temperature_2m_max,temperature_2m_min,apparent_temperature_max,apparent_temperature_min,sunrise,sunset,sunshine_duration,daylight_duration,uv_index_max,uv_index_clear_sky_max,rain_sum,showers_sum,snowfall_sum,precipitation_sum,precipitation_hours,precipitation_probability_max,wind_speed_10m_max,wind_direction_10m_dominant,wind_gusts_10m_max,shortwave_radiation_sum,et0_fao_evapotranspiration,wet_bulb_temperature_2m_mean,wet_bulb_temperature_2m_max,wet_bulb_temperature_2m_min,vapour_pressure_deficit_max,surface_pressure_mean,surface_pressure_max,surface_pressure_min,updraft_max,visibility_mean,visibility_min,visibility_max,winddirection_10m_dominant,wind_gusts_10m_mean,wind_speed_10m_mean,wind_gusts_10m_min,wind_speed_10m_min,et0_fao_evapotranspiration_sum,leaf_wetness_probability_mean,precipitation_probability_mean,precipitation_probability_min,growing_degree_days_base_0_limit_50,relative_humidity_2m_mean,relative_humidity_2m_max,relative_humidity_2m_min,temperature_2m_mean,apparent_temperature_mean,cape_mean,cape_max,cape_min,cloud_cover_mean,cloud_cover_max,cloud_cover_min,dew_point_2m_mean,dew_point_2m_max,dew_point_2m_min,snowfall_water_equivalent_sum,pressure_msl_mean,pressure_msl_max,pressure_msl_min&timezone=GMT&wind_speed_unit=mph&temperature_unit=fahrenheit 
        """
        try:
            #Make from system id
            message["id"] = self.system_id
            message["forecast_type"] = "daily"
            #Then the time:
            utc_curr_time = datetime.now(tz=pytz.UTC)
            time_string = utc_curr_time.strftime("%Y-%m-%dT%H:%M:%S.%f")
            message["time"] = time_string
            #Then the times
            day_list = message.get("daily", {}).get("time", [])
            try:
                message["first_time"] = day_list[0]
                message["last_time"] = day_list[-1]
            except Exception as e:
                logging.error(f"Issue parsing message time: {e}")
            daily_dict = message.get("daily", {})
            for field, time_list in daily_dict.items():
                if field == "time":
                    message["forecast_days"] = time_list
                else:
                    message[field] = time_list
            message.pop("daily", None)
        except Exception as e:
            logging.error(f"Error parsing open-meteo daily message {e}", exc_info=True)
        return message

    def parse_current(self, message):
        """
        Using JSON message format returned from this link:
        #https://api.open-meteo.com/v1/forecast?latitude=47.6825&longitude=-116.796944&current=temperature_2m,relative_humidity_2m,apparent_temperature,is_day,precipitation,rain,showers,snowfall,weather_code,cloud_cover,pressure_msl,surface_pressure,wind_speed_10m,wind_direction_10m,wind_gusts_10m&timezone=GMT&wind_speed_unit=mph&temperature_unit=fahrenheit 
        """
        try:
            #Make from system id e 
            message["id"] = self.system_id
            message["forecast_type"] = "current"
            #Then the time:
            utc_curr_time = datetime.now(tz=pytz.UTC)
            time_string = utc_curr_time.strftime("%Y-%m-%dT%H:%M:%S.%f")
            message["time"] = time_string
            current_dict = message.get("current", {})
            for field, val in current_dict.items():
                if field == "time":
                    message["forecast_time"] = val
                else:
                    message[field] = val
            message.pop("current", None)
        except Exception as e:
            logging.error(f"Error parsing open-meteo current message {e}", exc_info=True)
        return message


    def process_open_meteo_message(self, message_type, messages):
        """
        This function takes in a message_type and a list of messages
        It returns a list of messages, processed in some way 
        """
        try:
            for message in messages:
                new_message = {}
                sub_message = message.get("msg_content", {})
                if message_type == "open_meteo_daily_forecast":
                    new_message = self.parse_daily(sub_message)
                elif message_type == "open_meteo_current": 
                    new_message = self.parse_current(sub_message) 
                
                if new_message == {}:
                    #logging.debug(f"Error processing message")
                    return [] 
                message = self.envelope_id_override(message, new_message)
                logging.info(f"{message_type} Reading from Open-Meteo: {message}")
            return messages
        except Exception as e:
            logging.error(f"Could not process open-meteo messages: {e}")
            return [] 
        

def return_object(config={}, send_addresses={}, receive_addresses={}, message_configs={}):
    return OpenMeteo(config=config, send_addresses=send_addresses, receive_addresses=receive_addresses, message_configs=message_configs)

