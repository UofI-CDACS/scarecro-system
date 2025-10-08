# BLE Carrier
This carrier can listen specifically for the renogy sensor using BLE.  It can either listen for broadcast messages without a connection or form a specific connection to listen on. 

## Filename
src/carriers/
- BLE.py

## Dependencies
- You will need bluetooth enabled on your system 
- Other python libraries you will need include:
    - sys
    - time
    - logging
    - json
    - asyncio
    - bleak
    - os 

## Carrier Configuration Info:
- "source": "BLE" 
-  "read_method": ("beacon" or "write_read" or None) the method of connection the BLE will be reading for.  **Default**: None
    - if the method is "beacon", the addresses associated with this carrier will need the "data_uuid" of what to read
    - if the method is "write_read", the addresses associated with this carrier will need the "write_uuid" of the data to write, the "data_to_write", and the "data_uuid" of the data to read. 
- "listening interval": (Number) how long the BLE will listen for the messages in seconds when awake **Default**: 30 (note that you will want the receive function to less often than the listening interval or you may have collision issues). 

- Example (Beacon): 
/configs/carriers/:
**ble_beacon.json**:

        {
            "source": "BLE",
            "read_method": "beacon",
            "listening_interval": 20
        }   


- Example (Write Read): 
/configs/carriers/:
**ble_write_read.json**:

        {
            "source": "BLE",
            "read_method": "write_read",
            "listening_interval": 90
        }



## Send/Receive and Durations: 
- receive:
    - all durations supported 
- send: 
    - not currently supported for this carrier 

## Address Configurations: 
- in the "additional_info" section:
    - "data_uuid": (String or None) the data, in string value, of the BLE uuid to read from. **Default**: None
    - "connection": (True/False) Whether or not the sensor needs to be connected to in order to read from it **Default**: False
    - "write_uuid": (String or None) The uuid of where the data need to be written **Default**: None
    - "data_to_write": (List of Numbers or None) The data to write to the write_uuid **Default**: None
    - "mac_addresses": (List of Strings) List of mac addresses to filter by (or connect to) - needed for read_write **Default**: [] (empty list)
     

- Example (Beacon): 
**kkm_ble_in.json**:

        {
            "inheritance":[],
            "message_type": "kkm_k6p",
            "handler": "$msg_type",
            "handler_function": "process",
            "send_or_receive": "receive",
            "carrier": "ble_beacon",
            "duration": 300,
            "additional_info": {
                "data_uuid": "0000feaa-0000-1000-8000-00805f9b34fb",
                "connection": false
            } 
        }


- Example (Read_Write):
**renogy_ble_in.json**:

        {
            "inheritance":[],
            "message_type": "renogy_solar_charger",
            "handler": "$msg_type",
            "handler_function": "process",
            "send_or_receive": "receive",
            "carrier": "ble_write_read",
            "duration": 30,
            "additional_info": {
                "data_uuid": "0000fff1-0000-1000-8000-00805f9b34fb",
                "connection": true,
                "write_uuid": "0000ffd1-0000-1000-8000-00805f9b34fb",
                "data_to_write": [255, 3, 1, 0, 0, 34, 209, 241],
                "mac_addresses": ["find_your_sensors_mac_and_put_it_here"]
            } 
        }

## Other Functionality: 
- No other functionality implemented for this driver. 

## Behavior: 
- If duration is "always" for a beacon read, there will be a 1 minute (60 second) sleep between scans
- If duration is "always" for a write_read read, there will be a 5 minute (300 second) sleep between readings 
- TODO: Not sure we are actually using the conenction variable for anything 
- The renogy solar charger in particular has an odd bluetooth disconnect problem that sometimes requires restarting the bluetooth on the system. If the carrier runs into errors, it will try to restart the system bluetooth to solve this. If that causes other issues in your setup, please be aware. 
- The message from the BLE device read in from this carrier will usually take the form:

        {
            "name": name,
            "mac_address": address,
            "rssi": rssi,
            "packet": packet
        }

for a beacon, and:

        {
            "mac_address": address,
            "packet": packet
        }

for write_read. The parsing of the packet is left up to the associated handler. 


## Tested 
- kkm k6p beacon
- renogy solar charger (BT-1)


