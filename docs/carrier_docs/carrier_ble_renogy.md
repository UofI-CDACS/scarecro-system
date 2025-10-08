# BLE Carrier
This carrier can listen for sensors using BLE. It was implemented as its own carrier due to the complexity of the renogy sequence with Bleak.

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
    - os
    - threading 
    - libscrc
    - gatt 

## Carrier Configuration Info:
- "source": "BLE_renogy" 
- "listening interval": (Number) how long the BLE will listen for the messages in seconds when awake **Default**: 30 (this carrier only implemented for 'always' duration). 

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
**ble_renogy.json**:

    {
        "source": "BLE_renogy",
        "listening_interval": 60
    }


## Send/Receive and Durations: 
- receive:
    - only 'always' duration supported 
- send: 
    - not currently supported for this carrier 

## Address Configurations: 
- in the "additional_info" section:
    - "data_uuid": (String or None) the data, in string value, of the BLE uuid to read from. **Default**: None
    - "connection": (True/False) Whether or not the sensor needs to be connected to in order to read from it **Default**: False
    - "write_uuid": (String or None) The uuid of where the data need to be written **Default**: None
    - "data_to_write": (List of Numbers or None) The data to write to the write_uuid **Default**: None
    - "mac_addresses": (List of Strings) List of mac addresses to filter by (or connect to) - needed for read_write **Default**: [] (empty list)
    - "alias": string match of the device alias to listen for. 
    - TODO: alias should also probably be a list 
     

- Example (Beacon): 
**kkm_ble_in.json**:

    {
        "inheritance":[],
        "message_type": "renogy_solar_charger",
        "handler": "$msg_type",
        "handler_function": "process",
        "send_or_receive": "receive",
        "carrier": "ble_renogy",
        "duration": "always",
        "additional_info": {
            "data_uuid": "0000fff1-0000-1000-8000-00805f9b34fb",
            "connection": true,
            "write_uuid": "0000ffd1-0000-1000-8000-00805f9b34fb",
            "data_to_write": [255, 3, 1, 0, 0, 34, 209, 241],
            "mac_addresses": ["your_mac"],
            "alias": "your_alias"
        } 
    }




## Other Functionality: 
- No other functionality implemented for this driver. 

## Behavior: 
- The Bleak implementation for renogy solar charger BT-1 is highly unreliable. This implements the drive using the gatt library instead, which has been more stable for our testing. 
- The renogy solar charger in particular has an odd bluetooth disconnect problem that sometimes requires restarting the bluetooth on the system. If the carrier runs into errors, it will try to restart the connection. If that causes other issues in your setup, please be aware. 
- The message from the BLE device read in from this carrier will take the form:

        {
            "mac_address": address,
            "packet": packet
        }

for write_read. The parsing of the packet is left up to the associated handler. 


## Tested 
- renogy solar charger (BT-1)

