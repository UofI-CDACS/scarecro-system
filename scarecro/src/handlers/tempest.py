from datetime import datetime, timedelta, tzinfo
from datetime import timezone
from datetime import date
import pytz
from dateutil import tz 
import logging 


class Tempest:
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
        logging.info("Initing Tempest Forecast handler")
        #Not sure we need the system ID 
        #Put in the system id 
        #self.system_id = self.config.get("system_id", "default")
    

    def envelope_id_override(self, message_envelope, message_content): 
        message_def = self.message_definitions.get(message_envelope.get("msg_type", None), {})
        message_envelope["msg_content"] = message_content
        message_envelope["msg_id"] = message_content.get(message_def.get("id_field", "id"), "default")
        message_envelope["msg_time"] = message_content.get(message_def.get("time_field", "time"), "default")
        return message_envelope

    def parse_station_obs(self, message):
        """
        Parsing Tempest Latest Station Observation
        """
        try:
            #Make from system id
            message["id"] = message.get("station_id", None)
            #Then the time:
            utc_curr_time = datetime.now(tz=pytz.UTC)
            time_string = utc_curr_time.strftime("%Y-%m-%dT%H:%M:%S.%f")
            message["time"] = time_string
            #Then the obs
            obs = message.get("obs", [False])[0]
            if obs:
                for key, value in obs.items():
                     message[key] = value
            else:
                logging.error(f"Issue with observations in Tempest message")
            
            message.pop("obs", None)
            message.pop("station_units", None)
            message.pop("outdoor_keys", None)
            message.pop("status", None)
        except Exception as e:
            logging.error(f"Error parsing tempest latest station observation message {e}", exc_info=True)
        return message


    def parse_broader_station_obs(self, message):
        """
        Parsing Tempest Broader Station Observation
        """
        try:
            #Make from system id
            message["id"] = message.get("station_id", None)
            #Then the time:
            utc_curr_time = datetime.now(tz=pytz.UTC)
            time_string = utc_curr_time.strftime("%Y-%m-%dT%H:%M:%S.%f")
            message["time"] = time_string
            #Then the times
            ob_fields = message.get("ob_fields", False)
            obs = message.get("obs", [False])[0]
            if ob_fields and obs:
                for i in range(0, len(ob_fields)):
                     message[ob_fields[i]] = obs[i]
            else:
                logging.error("Issue with observations in Tempest message")
            
            message.pop("ob_fields", None)
            message.pop("obs", None)
            message.pop("units", None)
            message.pop("status", None)
        except Exception as e:
            logging.error(f"Error parsing tempest latest station observation message {e}", exc_info=True)
        return message

    def parse_forecast(self, message):
        """
        Parsing Tempest Better Forecast 
        """
        try:
            
            #Then the time:
            utc_curr_time = datetime.now(tz=pytz.UTC)
            time_string = utc_curr_time.strftime("%Y-%m-%dT%H:%M:%S.%f")
            message["time"] = time_string
            #Then the current_conditions
            current_conditions = message.get("current_conditions", {})
            for key, value in current_conditions.items():
                message[f"curr_{key}"] = value
            #Station Values
            station = message.get("station", {})
            for key, value in station.items():
                message[f"{key}"] = value
            #Make from system id
            message["id"] = message.get("station_id", "default")
            #Forecast
            forecast = message.get("forecast", False)
            if forecast:
                #Daily 
                daily_forecast = forecast.get("daily", [False])
                first_day = daily_forecast[0]
                if first_day:
                    for key, value in first_day.items():
                        message[f"day_{key}"] = []
                    for day in daily_forecast:
                        for key, value in day.items():
                            message[f"day_{key}"].append(value)
                #Hourly 
                hourly_forecast = forecast.get("hourly", [False])
                first_hour = hourly_forecast[0]
                if first_hour:
                    for key, value in first_hour.items():
                        message[f"hour_{key}"] = []
                    for hour in hourly_forecast:
                        for key, value in hour.items():
                            message[f"hour_{key}"].append(value)
            else:
                logging.error("Issue with observations in Tempest Forecast message")
            message.pop("forecast", None)
            message.pop("units", None)
            message.pop("status", None)
        except Exception as e:
            logging.error(f"Error parsing tempest forecast message {e}", exc_info=True)
        return message

    def process_tempest_message(self, message_type, messages):
        """
        This function takes in a message_type and a list of messages
        It returns a list of messages, processed in some way 
        """
        try:
            for message in messages:
                new_message = {}
                sub_message = message.get("msg_content", {})
                if message_type == "tempest_station":
                    new_message = self.parse_station_obs(sub_message)
                elif message_type == "tempest_forecast": 
                    new_message = self.parse_forecast(sub_message) 
                
                if new_message == {}:
                    #logging.debug(f"Error processing message")
                    return [] 
                message = self.envelope_id_override(message, new_message)
                if message_type != "tempest_forecast":
                    logging.info(f"{message_type} Reading from Tempest: {message}")
            return messages
        except Exception as e:
            logging.error(f"Could not process tempest messages: {e}")
            return [] 
        

def return_object(config={}, send_addresses={}, receive_addresses={}, message_configs={}):
    return Tempest(config=config, send_addresses=send_addresses, receive_addresses=receive_addresses, message_configs=message_configs)

