# Renogy Solar Charger Handler
This handler processes messages that come from the raw bluetooth read for the renogy solar charger sensor. 

## Filename
src/handlers/
- renogy_solar_charger.py

## Dependencies
- python libraries you will need include:
    - logging
    - sys 
  

## Handler Configuration Info:
- "source": "renogy_solar_charger" 

- Example: 
/configs/handlers/:
**renogy_solar_charger.json**:

        {
            "source": "renogy_solar_charger"
        }

## Processing Functions 
-  process is the only function used to process renogy solar charger messages

## Carrier Configuration Needs
- no specific needs, but this handler is meant specifically to parse a BLE packet 

## Address Configurations: 
- no additional address configuration needs for this handler 
- Example: 
**renogy_ble_inbound.json**:

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
        "mac_addresses": ["a_renogy_mac"]
    } 
}


## Other Functionality: 
- No other functionality implemented for this carrier. 

## Behavior: 
- The handler heavilty relies on [this code from this github repo for Renogy BT1](https://github.com/cyrils/renogy-bt/tree/main/renogybt)
- envelope overrides the ID after parsing it out 

## Tested 
- renogy_solar_charger BT1 module 

