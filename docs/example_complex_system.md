# Example Complex System - Gateway and Middle Agent 


## Gateway - Sensors


## Equipment 
- This guide assumes you are planning to use the setup for the solar-powered raspberry pi gateway, which you [check out how to build here]()
- This guide also assumes you have the gateway software set up, [which you can check out here]()


## Configurations 
For ease of setup, the complete configurations for this setup are located in the [example data folder located here](../scarecro/examples/example_configs/solar_powered_gateway/)

### Messages
In /configs/messages/
- default_sensor.json

        {
            "id_field": "id",
            "time_field": "time"
        }

- gateway_stats.json
        
        {
            "inheritance": ["default_sensor"]
        }


- renogy_solar_charger.json  

        {
            "inheritance": ["default_sensor"]
        }

### Carriers
In /configs/carriers/
- ble_write_read.json

        {
            "source": "BLE",
            "read_method": "write_read",
            "listening_interval": 90
        }

- mqtt_cloud.json

        {
            "source": "mqtt",
            "mqtt_url": "your_cloud_mqtt_url",
            "mqtt_port": 8883,
            "mqtt_username": "your_mqtt_username",
            "mqtt_password": "your_mqtt_password",
            "qos": 1,
            "client_id": "sensor_sender",
            "version": 5,
            "system_id": "$system_id",
            "monitor_connection": false
        }

- underlying_system.json 

        {
            "source": "underlying_system",
            "id": "$system_id"
        }

### Handlers
In /configs/handlers/
- renogy_solar_charger.json 

        {
            "source": "renogy_solar_charger"
        }

### Tasks
In /configs/tasks/
- fan_check.json

        {
            "source": "fan",
            "function": "fan_check",
            "arguments": {},
            "duration": 60,
            "fan_on_temp": 37.0,
            "fan_off_temp": 34.0,
            "power_pins": [18, 5]
        }

- pat_watchdog.json

        {
            "source": "watchdog",
            "function": "pat_the_dog",
            "arguments": {},
            "duration": 15,
            "pin": 4
        }

### Addresses
In /configs/addresses/
- gateway_stats_in.json

        {
            "inheritance":[],
            "handler": null,
            "handler_function": null,
            "send_or_receive": "receive",
            "message_type": "gateway_stats",
            "carrier": "underlying_system",
            "duration": 300,
            "additional_info": {
                "function": "status_reading"
            } 
        }

- renogy_ble_in.json 

        {
            "inheritance":[],
            "message_type": "renogy_solar_charger",
            "handler": "$msg_type",
            "handler_function": "process",
            "send_or_receive": "receive",
            "carrier": "ble_write_read",
            "duration": 300,
            "additional_info": {
                "data_uuid": "0000fff1-0000-1000-8000-00805f9b34fb",
                "connection": true,
                "write_uuid": "0000ffd1-0000-1000-8000-00805f9b34fb",
                "data_to_write": [255, 3, 1, 0, 0, 34, 209, 241],
                "mac_addresses": ["your_renogy_mac_address"]
            } 
        }

- cloud_mqtt_send_immediate.json 

        {
            "inheritance":[],
            "message_type": [
                "gateway_stats",
                "renogy_solar_charger",
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

### System 
/configs/system/

**system.json**

    {
        "id": "gateway_id",
        "addresses": [
            "gateway_stats_in",
            "renogy_ble_in,
            "cloud_mqtt_send_immediate"
        ],
        "tasks": [
            "fan_check",
            "pat_watchdog"
        ]
    }

## Source Code File Needs 
These source code files should already come in with your scarecro system download, but you may want to verify that you have the following: 

/src/
- carriers/
    - BLE.py
    - mqtt.py 
    - underlying_system.py 
- handlers/
    - renogy_solar_charger.py 
- tasks/
    - fan.py
    - watchdog.py 



## To Run: 

Inside scarecro/

```bash
    python3 scarecro.py 
```

You can also run it as a service [by following the instructions here]()


TODO: Test 
TODO: Link more documentation 