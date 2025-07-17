# Example System Configuration  
This guide will go over how the SCARECRO system is set up and configured based on your needs. We will go over a "hypothetical" example of potential system needs. 

## Scenario
Let's say you're an apple orchard manager who has a business case to start collecting some data from the field. You have done your research, and decide that you want to collect the following sensor data:
- temperature and humidity data from 20 kkm_k6p beacons, reporting on BLE (5 minute resolution)
- pressure data from a bmp280 pressure sensor (10 minute resolution)

You decide to use a SCARECRO raspberry pi gateway station to collect the data, and you want to store your data in a local MongoDB database. 

How do you set up the system? 

## First - Your Message Configurations
You know the basic format of the messages coming in from the kkm_k6p temp/humidity sensor and the bmp280 pressure sensor. The first thing you need to do is configure these messages and put them in your system. 

[You can see more about how messages work here](messages.md)

Basically, you need two json files in the configs/messages/ folder in the downloaded scareco system software that are named for your messages. These messages need to have an id_field and a time_field identified. For both of these, the "id_field" in the message is just going to be "id", and the time field is just going to be "time". This is the same as the default sensor. So, you can just have the json file inherit these properties. For more information on keyword substitution and inheritance, [check out this documentation page](configuration_inheritance_and_keyword_substitution.md) You already have a file in configs/messages that looks like:

**default_sensor.json**

    {
        "id_field": "id",
        "time_field": "time"
    }

So you add your two new message files: 

**kkm_k6p.json**

    {
        "inheritance": ["default_sensor"]
    }

**bmp280.json**

    {
        "inheritance": ["default_sensor"]
    }

Now, your messages are configured. 

## Second - Your Carrier Configurations
Now, you need to configure some carriers. Carriers are the communication protocols that will allow you to connect to your sensors. [You can see more about how carriers work here](carrier_class.md) You know that:
- kkm_k6p sensors connect via BLE
- bmp280 is a wired i2c device.  

You look through the TODO: LINK [implemented carrier documentation]() and see that there is a BLE carrier and an i2c carrier. 

### BLE Carrier Configuration
The BLE carrier expects (from the carrier):
- the read_method ("beacon" or "write_read")
- the listening interval (in seconds)

and, when you create an address using this carrier, it will expect (from a beacon sensor): 
- the uuid of data to read 
- connection (true or false), which denotes whether or not you need to connect the sensor. 

The kkm_k6p is a beacon sensor, so you decide to create a BLE carrier (stored in configs/carriers/) configured this way:

**ble_beacon.json**

    {
        "source": "BLE",
        "read_method": "beacon",
        "listening_interval": 15
    }

This will use the BLE carrier source code. It will set the read method as beacon, and the listening interval at 15 (it will listen for data from the addresses you give for about 15 seconds total when it is run)

### i2c Carrier Configuration  
Next, you notice that there is an i2c carrier. It the carrier class does not expect much. 

From the carrier:
- optionally, you can give it the system id

From the address:
- you will need to give it the i2c_address of the sensor 

So, you create a carrier named i2c stored in (/configs/carriers/) that looks like:

**i2c.json**

    {
        "source": "i2c",
        "id": "$system_id"
    }

## Third - Your Handler Configurations 
Now, you have your carrier and message configuration, you need to see if your sensors are going to take some difficult data translation/processing. [You can see more about how handlers work here](handler_class.md) You notice the bmp280 data manipulation is handled inside the carrier, and does not need anything extra. However, the kkm_k6p packet is tricky to translate, and you will need the kkm_k6p-specific byte formatting to do this effectively. You decide to make an instance of the kkm_k6p handler to do this. This handler configuration does not expect much, just the source code file name. So, in configs/handlers/, you create this file:

**kkm_k6p.json**

    {
        "source": "kkm_k6p"
    }

You are now finished configuring your handlers. 

## Fourth - Address Configurations
You now need to tie these together. [You can see more about how addresses work here](addresses.md) You need two addresses, one that routes your kkm_k6p data, and one that routes your bmp280 data. You know the BLE carrier needs the uuid and connection data, and the i2c carrier needs the i2c address of the sensor. So, in /configs/addresses/, you make the following two files: 

**kkm_ble_in.json**

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

This address says:
- the message that will be routed is a "kkm_k6p" message
- messages will be **received** on the "ble_beacon" carrier
- it will be handled by a handler with the same name as the message (substituted here - for more information on keyword substitution and inheritance, [check out this documentation page](configuration_inheritance_and_keyword_substitution.md))
- the handler function that will be used to process the message is named "process"
- the carrier will try to receive this message every 300 seconds, or 5 minutes
- the carrier will use the given uuid (which you find in kkm_k6p documentation) to try and find this particular type of message
- the carrier will not expect to have a persistent connection with the device 

**bmp280_in.json**

    {
        "inheritance": [],
        "handler": null,
        "handler_function": null,
        "send_or_receive": "receive",
        "message_type": "bmp280",
        "carrier": "i2c",
        "duration": 600,
        "additional_info": {
            "i2c_address": 119
        }
    }

This address says:
- This address will be receiving a "bmp280" type message
- It will be **received** on the i2c carrier
- The carrier will run the recieve function every 600 seconds (or 10 minutes)
- No handlers are needed to process the message
- The i2c carrier is expecting to recieve the i2c address of the sensor, which is 119 in this case. 

## Fifth - System Configuration
Now, you can quickly check that everything aligns. All your configurations for carriers and handlers should have the appropriate source code files in the /src/carriers/ and /src/handlers/ folder. Since you have a ble carrier and an i2c carrier, you should have in /src/carriers/:
- BLE.py
- i2c.py

And in /src/handlers/
- kkm_k6p.py 

Now, in /configs/system/, you just need to note what addresses you plan to use in the system. [You can see more about how the system class works here](system_class.md) Your system config will look like: 

**system.json**

    {
        "id": "gateway_id",
        "addresses": [
            "kkm_ble_in",
            "bmp280_in
        ]
    }

Where "id" is the id of your overall scarecro collection device, and the addresses are the configured addresses you made and want to be active in your system. 

Now, if you go inside the scarecro folder and run 

```bash
    python3 scarecro.py
```

Your system would start collecting from the kkm_k6p sensor and the bmp280 sensor and storing the data in it's message table. 

## Sixth - But Wait -- Where do you store your data??
You may have noticed, we can get the sensor information **in** now, but we aren't **storing** it anywhere. We need to to figure out how we want this information routed for storage. This will involve a new carrier and a new address. 

We decide we want every message we read in to be stored in a local mongodb database we have installed on our system. We notice that there is a mongodb carrier already implemented, and it expects from a carrier configuration:
- source code file name
- connection_url to the mongodb database
- version of mongodb to use
- database_name to write to
- persistent connection
- number of days to retain the data 

and for the address using this carrier:
- collection name the message will go to. 

### Configuring the Carrier
We add a mongodb carrier configuration to our /configs/carriers/ folder:

**mongodb_local.json**

    {
        "source": "mongodb",
        "connection_url": "127.0.0.1",
        "database_name": "SCARECRO",
        "version": 2.4, 
        "persistent_connection": true,
        "retain_days": 30
    }

Note, the raspberry pi we plan to use only supports a pretty old version of mongo, but the source code can handle that. 

### Configuring the data storage address
Now, we want to decide how to store our data. We could have mongo check the message table every 5 or so minutes and add readings, but we have decided our messaging rates using our carriers. So, we decide that **every message** that comes in to the system's message table should be stored in our local mongodb database. So, we create the following address in /configs/addresses/:


**mongo_local_immediate.json**

    {
        "inheritance":[],
        "message_type": [   
            "kkm_k6p",
            "bmp280",
        ],
        "handler": null,
        "handler_function": null,
        "send_or_receive": "send",
        "carrier": "mongodb_local",
        "duration": "on_message",
        "additional_info": {
            "collection": "$msg_type"
        } 
    }

This address says:
- any time the system sees the "kkm_k6p" message or "bmp280" message in the message table, immediately **send** it to the local mongodb carrier 
- no handler is needed for either of these messages (remember, by the time the kkm_k6p message gets to the message table, it's already been processed/translated by the incoming handler)
- the mongodb carrier expects information on what collection it should store it to, and in this case, we want to the collection name to be the same as the message type (substituting it)

Since we added the carrier config, we need to be sure that in /src/carriers/, we have a code file named "mongodb.py" which implements our carrier class. 

### Updating the System Config
Now, we need to make sure the system config uses this new address. We will update it in /configs/system/

**system.json**

    {
        "id": "gateway_id",
        "addresses": [
            "kkm_ble_in",
            "bmp280_in,
            "mongo_local_immediate"
        ]
    }


Now, if you go inside the scarecro folder and run 

```bash
    python3 scarecro.py
```

It will collect data from the kkm_k6p beacons every 5 minutes, collect data from the bmp280 sensor every 10 minutes, and every time it collects a new message, will store it to the local mongodb database. 

## Seventh - Testing in Debug Mode
One useful way to test your scarecro system setup is to try out your system configuration in debug mode. One way to do this is to write out the system configuration in a dictionary and add your setup into the tests folder. Inside the tests folder is (TODO: Add testing documentation) a file called **configuration_tester.py** which has a handy function:

    run_test_configuration(system_config)

You can import and pass your system config. This will run the SCARECRO system with your configuration in debug mode. You could make a python file:

**test_my_custom_config.py**


    import configuration_tester
    system_config = {
        "id": "gateway_id",
        "addresses": [
            "kkm_ble_in",
            "bmp280_in,
            "mongo_local_immediate.json"
        ]
    }
    configuration_tester.run_test_configuration(system_config)

To check it out by running:

```bash
    python3 tests/test_my_custom_config.py
```


Debug mode:
- Prints the system storage of configs and objects on start-up
- Prints the messaging table after each message receipt 

## Finally - Running the Service 

TODO: scarecro.service file

## Try it
If you would like to run this particular example (recommended on a raspberry pi), 
the config files are stored are **/example_data/example_configs/basic_kkm_bmp280_data_logger/**


## More Examples 
- Very basic system
- Configuring just a solar powered gateway 
- Configuring just an web API machine 
- Configuring a gateway and a cloud agent (more advanced)

## Notes on Usage 
You can see from this example that there is some significant overhead for a fairly simple sensor process. The SCARECRO is indeed some hefty overhead for minor functionality - the system is more useful in the cases where:
- the number and types of sensors are more complex, or
- multiple types of wireless communication protocols are used, or 
- there is a wide variety of communication rates, or 
- the same communication protocol is used for different sensors/rates, or
- you have limited experience setting up wireless communication, or
- you want to reuse existing upstream data infrastructure to the extent possible 


## TODO: 
TODO: Integrating a New Sensor or Communication Protocol 
TODO: Add documentation links to different system classes.  
TODO: In-depth diagrams 
