## Addresses
The address configuration is necessary to actually send and receive messages, and ties together carriers, handlers, and messages. Addresses essentially denote the necessary informatin routing for the entire system, and 

## Address Configuration 

[For inheritance and keyword substitution, see this file](configuration_inheritance_and_keyword_substitution.md) 

Addresses should be a dictionary of the following form:

{
    "inheritance": a name of list of other names addresses to inherit from

    "message_type": the type of message this address deals with. If this is a list, the underlying system will break the address into multiple addresses by message type, naming them <address_name>_<message_type>. An address cannot inherit from another address with multiple messages. 

    "handler": the name of the handler config for this message before send/after receive. This can be None, if no processing is needed. 

    "handler_function": the function in the processing object that will receive the message for processing as its argument. 

    "send_or_receive": "send" or "recieve", indicating whether the is the receiving address for a message or the sending addresses for a message

    "carrier": The object that will send or receive the message.

    "duration": How often the message is sent through the system. This can be:
         "always", if the message is always being sent or recieved, 
          a value in seconds, for how often the message is being sent or received, 
          "on_message", for a sender that sends on every new message coming through, or
          "as_needed", if the send or received is triggered by something else on an as_needed basis 
    }
    
    "additional_info": This is any additional information that may be needed to send the message effectively. This might be message-specific endpoint information, for example, for a sender or receiver. This will likely vary by carrier. 


## Example Address 1:

cloud_mqtt_send_immediate.json: 

    {
        "inheritance":[],
        "message_type": [
            "atlas_gravity_ph",
            "atlas_ezo_ph",
            "meter_teros10",
            "kkm_k6p",
            "generic_pH",
            "minew_s1",
            "datagator",
            "datagator_ota",
            "gateway_stats",
            "bmp280",
            "image_info",
            "renogy_solar_charger",
            "weather_rack",
            "local_config_updated",
            "recovery_data_request",
            "recovery_data",
            "confirm_receipt"
            ],
        "handler": null,
        "handler_function": null,
        "send_or_receive": "send",
        "carrier": "mqtt_cloud",
        "duration": "on_message",
        "additional_info": {
            "topic": "$msg_type"
        } 
    }

This address is used to send multiple messages on the mqtt cloud carrier whenever a message comes in. It inherits from nothing and has no handler, and the carrier needs an additional piece of info (the topic) which will correspond to the message_type (substituted when the address is resolved)

## Example Address 2: 

weather_rack_433_in.json:

    {
        "inheritance":["switchdoc_sensors_in"],
        "message_type": "weather_rack",
        "additional_info": {
            "string_matches": ["SwitchDoc Labs FT020T AIO"],
            "driver": 146
        } 
    }

This address inherits from an address config named switchdoc_sensors_in, which handles some of the missing values. It needs the message type, and also has some additional needed info for the carrier involving the string matches and driver number to use. 

Then, **switch_doc_sensors_in.json** looks liek:

    {
        "inheritance":[],
        "handler": "switchdoc_handler",
        "handler_function": "process_switchdoc_sensor_message",
        "send_or_receive": "receive",
        "carrier": "433_listener",
        "duration": "always"
    }

Where the switchdoc handler (using the **process_switchdoc_sensor_message** function) is used for data transformation, and the 433_listener carrier (which always run, hence the "always" keyword) receives the message. 

## See Also
TODO 