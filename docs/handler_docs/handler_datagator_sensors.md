# Datagator Sensors Handler
This handler processes messages in particular that come from SCARECRO's Data Gator aggregation module.  

## Filename
src/handlers/
- datagator_sensors.py

## Dependencies
- python libraries you will need include:
    - datetime
    - pytz
    - dateutil
    - logging
  

## Handler Configuration Info:
- "source": "datagator_sensors" 

- Example: 
/configs/handlers/:
**datagator_sensors.json**:

        {
            "source": "datagator_sensors"    
        }

## Processing Functions 
-  process_datagator_sensor_message is the only directly used processing function. It takes the message type and list of messages (as is defined for handlers) and uses the message type to decide how to process

## Carrier Configuration Needs
"include_topic" key should set to "True" on an mqtt carrier. 

## Address Configurations: 
- no additional address configuration needs for this handler 
- Example: 
**meter_teros10_inbound_datagator.json**:

        {
            "inheritance":[],
            "message_type": [
                "meter_teros10",

            ],
            "handler": "datagator_sensors",
            "handler_function": "process_datagator_sensor_message",
            "send_or_receive": "receive",
            "carrier": "local_inbound_mqtt",
            "duration": "always",
            "additional_info": {
                "topic": "$msg_type"
            } 
        }


## Other Functionality: 
- No other functionality implemented for this carrier. 

## Behavior: 
- The handler will replace the id of the message with the mac address of the sensor in most cases. It may use the data gator's mac and the port level to create a unique id depending on the sensor 
- Data Gator sensor often need the passed-in "topic" of the mqtt message. So, you will want "include_topic" set to "True"
on a carrier. 
- This driver will override the system envelope with the parsed content. 

## Tested 
- datagator (tlm and ota)
- atlas_gravity_ph
- atlas_ezo_ph
- meter_teros10
- mij_02_lms
- kkm_k6p
- generic_pH
- minew_s1 


