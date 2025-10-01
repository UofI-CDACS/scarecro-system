import sys
import time 
import requests
import logging 
import json 
sys.path.append("../scarecro")
import system_object
import util.util as util 
#Help from the documentation here: https://www.eclipse.org/paho/index.php?page=clients/python/docs/index.php#multiple

class API():
    def __init__(self, config, send_addresses, receive_addresses, message_configs):
        """
        API does not need anything specific in the carrier config 
        API needs in its  addresses config:
        "request_type": (string, "GET", or "POST") a list of strings that the incoming json message can match to identify it (**default in carrier**: "GET")
        "url": (List of strings, String, or None) the url (or list of them) of the endpoint to ping (**Default**: None) NOTE: This url would include any arguments or authorization tokens, as there is no parsing or combination mechanisms currently implemented in the carrier. If you need more complex behavior, we would recommend making an api-specific carrier for the endpoint(s) you plan to use 
        "headers" (dict, or None): A dictionary of header names and string values, in the format expected by the python requests dictionary, for the given api (**Default**: None) (POST only)
        "data": (string, or None): A string of the data to send via the post request (**Default**: None) (POST only)
        """
        #arguments passed in 
        self.config = config 
        self.send_addresses = send_addresses 
        self.receive_addresses = receive_addresses
        self.message_configs = message_configs
        self.mapping_dict = util.forward_backward_map_additional_info([self.send_addresses, self.receive_addresses])


    def disconnect(self):
        """
        In current implementation, function takes no arguments
        And only prints a message to the console. 
        """
        logging.info("Disconnect API: No actions needed for API disconnect in this driver.")  

    def process_get_request(self, address_name, url):
        """
        Takes in an address name, url, gets data needed to get a response 
        using a get request 
        """
        response = {}
        try:
            response = requests.get(url)
        except Exception as e:
            logging.error(f"Could not process GET request for {address_name}: {e}", exc_info=True)
        return response 

    def process_post_request(self, address_name, url):
        """
        Takes in an address name, url, gets data needed to get a response 
        using a post request
        """
        response = {}
        try:
            headers = self.mapping_dict.get("headers", {}).get("address_name", {}).get(address_name, None)
            data = self.mapping_dict.get("data", {}).get("address_name", {}).get(address_name, None)
            if headers == None and data == None:
                response = requests.post(url) 
            elif headers == None:
                response = requests.post(url, data=data) 
            elif data == None:
                response = requests.post(url, headers=headers) 
            else:
                response = requests.post(url, headers=headers, data=data) 
        except Exception as e:
            logging.error(f"Could not process POST request for {address_name}: {e}", exc_info=True)
        return response 


    def ping_api(self, address_name, url):
        """
        Takes in an address name and uses the configured address information to 
        ping an endpoint 
        Expects a response in json for now 
        """
        try:
            #Get the request type
            request_type = self.mapping_dict.get("request_type", {}).get("address_name", {}).get(address_name, "GET")
            #If the request type is GET, get from the URL
            if request_type == "GET":
                response = self.process_get_request(address_name, url)
            #TOD_ may want this in own body 
            elif request_type == "POST":
                response = self.process_post_request(address_name, url)
            else:
                logging.error(f"Request type {request_type} not understood")
                response = {}
            logging.debug(f"Response: {response}")
            #If we got a valid response
            if response != {}:
                if response.status_code == 200:
                    try:
                        message_body = response.json()
                        #If the message isn't empty 
                        if message_body != {}:
                            enveloped_message = system_object.system.envelope_message(message_body, address_name)
                            system_object.system.post_messages(enveloped_message, address_name)
                    except Exception as e:
                        logging.error(f"Could not post API message on address {address_name}: {e}", exc_info=True)
                #Otherwise, note the error
                else:
                    logging.error(f"Response code on address {address_name}: {response.status_code}")
        except Exception as e:
            logging.error(f"Error in ping api function for address {address_name}: {e}", exc_info=True)

    def handle_api_request(self, address_name):
        """
        Takes in an address name and decides to process one or multiple
        apis based on whether the url is a list or string
        """
        try:
            url = self.mapping_dict.get("url", {}).get("address_name", {}).get(address_name, None)
            if isinstance(url, list):
                for individ_url in url:
                    self.ping_api(address_name, individ_url)
            else:
                self.ping_api(address_name, url)
        except Exception as e:
            logging.error(f"Could not handle api request: {e}")
        return 


    def receive(self, address_names, duration):
        """
        Receives a list of addresses (all with same duration). Depending 
        on the duration and the address, it sets itself
        up to 'receive' spoofed messages and post them
        to the system post office along with an address 
        """
        try:
            if duration == "always":
                for address_name in address_names:
                    self.handle_api_request(address_name)
                time.sleep(300)
            else:
                for address_name in address_names:
                    self.handle_api_request(address_name)
        except Exception as e:
            logging.error(f"Error in api receive {e}", exc_info=True)


    def send(self, address_names, duration, entry_ids=[]):
        """
        Takes in an optional list of entry ids
        Grabs the messages and publishes them, optionally filtering by ID 
        Not yet defined for this driver 
        """
        pass 


def return_object(config={}, send_addresses={}, receive_addresses={}, message_configs={}):
    return API(config=config, send_addresses=send_addresses, receive_addresses=receive_addresses, message_configs=message_configs)
