# KKM K6P Handler
This handler processes messages that come from the raw bluetooth read for the kkm k6p sensor. 

## Filename
src/handlers/
- kkm_k6p.py

## Dependencies
- python libraries you will need include:
    - logging
    - sys 
  

## Handler Configuration Info:
- "source": "kkm_k6p" 

- Example: 
/configs/handlers/:
**kkm_k6p.json**:

        {
            "source": "kkm_k6p"
        }

## Processing Functions 
-  process is the only function used to process kkm k6p messages

## Carrier Configuration Needs
- no specific needs, but this handler is meant specifically to parse a BLE packet 

## Address Configurations: 
- no additional address configuration needs for this handler 
- Example: 
**meter_teros10_inbound_datagator.json**:

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


## Other Functionality: 
- No other functionality implemented for this carrier. 

## Behavior: 
- The handler uses [some code from this github repo for Renogy](https://github.com/cyrils/renogy-bt/tree/main/renogybt)
- envelope overrides the ID after parsing it out 

## Tested 
- kkm_k6p

