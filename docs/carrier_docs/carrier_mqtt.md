# MQTT Carrier
This carrier can send messages using MQTT on either a local broker or a cloud broker. 

## Filename
src/carriers/
- mqtt.py

## Dependencies
- If you are planning to use a local broker on your system, you would need that installed. On the raspberry pi, we tend to use the mosquitto broker
TODO: Link [Check out the installation instructions for the library here]()
- Other python libraries you will need include:
    - sys
    - time
    - logging
    - json
    - paho-mqtt (different versions may have slightly different behavior, so be aware of this. For example, some paho versions do not support MQTT v5)

## Carrier Configuration Info:
- "source": "mqtt" 
-  "mqtt_url": (String) the url of the mqtt broker you will be connecting to. **Default**: "127.0.0.1" (the basic host machine)
- "mqtt_port": (Number) the numeric port the broker will be connected on. **Default**: 1883
- "mqtt_username": (String or None): the username used for the connection credentials for your broker. **Default**: None. Note: if the username or password is not set, it will attemp to connect without the tls protocol. 
- "mqtt_password": (String or None): the username used for the connection credentials for your broker. **Default**: None. Note: if the username or password is not set, it will attemp to connect without the tls protocol.
- "qos": (Number) the quality of service setting to use. **Default**: 1 
- "client_id": (String) the client id name you want to use when connecting to the broker. **Default**: "default" 
- "version": (Number) the version of mqtt you will use. **Default**: 5
- "system_id": (String) the system id, most likely passed through from the main system using keyword substitution. **Default**: "default"
- "monitor_connection": (True/False) whether or not the carrier will monitor it's connection status to the broker. **Default**: False
- "include_topic": (True/False) whether or not to pass the mqtt topic into the resultant message. **Default**: False  

- Example (Local): 
/configs/carriers/:
**local_inbound_mqtt.json**:

        {
            "source": "mqtt",
            "mqtt_url": "127.0.0.1",
            "mqtt_port": 1883,
            "qos": 0,
            "client_id": "sensor_listener",
            "version": 3, 
            "include_topic": true
        }

- Example (Cloud): 
/configs/carriers/:
**mqtt_cloud.json**:

        {
            "source": "mqtt",
            "mqtt_url": "cloud_broker_url",
            "mqtt_port": 8883,
            "mqtt_username": "your_username",
            "mqtt_password": "your_password",
            "qos": 1,
            "client_id": "sensor_sender",
            "version": 5,
            "system_id": "$system_id",
            "monitor_connection": true
        }


## Send/Receive and Durations: 
- receive:
    - all durations supported 
- send: 
    - "always" duration **is not supported**
    - durations which **return** (numeric seconds, on_message, as_needed) **are supported**

## Address Configurations: 
- in the "additional_info" section:
    - "topic": (String) the name of the mqtt topic the message will be sent or received on. **Default**: None
     

- Example (Local): 
**meter_teros10_inbound.json**:

        {
            "inheritance":[],
            "message_type": [
                "meter_teros10",
            ]
            "handler": "datagator_sensors",
            "handler_function": "process_datagator_sensor_message",
            "send_or_receive": "receive",
            "carrier": "local_inbound_mqtt",
            "duration": "always",
            "additional_info": {
                "topic": "$msg_type"
            } 
        }


- Example (Cloud):
**meter_teros10_outbound.json**:

        {
            "inheritance":[],
            "message_type": [
                "meter_teros10",
            ],
            "handler": null,
            "handler_function": null,
            "send_or_receive": "receive",
            "carrier": "mqtt_cloud",
            "duration": "always",
            "additional_info": {
                "topic": "$msg_type"
            } 
        }


## Other Functionality: 
- Please see the relevant documentation in the [implemented tasks section here](TODO) 
- Checking Connection (System type task, partly implemented in this carrier): [See the documentation for the recovery class here](../recovery.md). This uses:
    - the check_connection_status to check the connection status to the broker IF the monitor_connection paramter true. If it has lost connection, is posts a connection_status message with the disconnect field filled in. If the connection has been restored, it posts the appropriate restored connection message. 

## Behavior: 
- Monitor Connection: If monitoring connection is true, the class will check its connection to the broker and post the appropriate messages 
- If the gateway shuts down, it will try to disconnect itself from the connect mqtt brokers first. 

## Tested 
- All datagator-routed inbound sensors
- All outgoing sensor infrmation over cloud broker 

