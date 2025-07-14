# Configuration Inheritance and Keyword Substitution
To eliminate code duplication, the SCARECRO system allows:
- Inheriting from other configurations (in the same folder)
- Providing certain keyword substitutions 
Both features are designed to make simpler, more composable configurations. 

## Inheritance
Most configurations have a field called "inheritance". This links to an expected list of configurations to inherit from. 

For example, let's say we have an address configuration called fake_receive.py: 

    address = {
        "inheritance":[],
        "message_type": "test_message",
        "handler": "fake_message_handler",
        "handler_function": "process",
        "send_or_receive": "receive",
        "carrier": "fake_message_listener",
        "duration": 10,
    }

And then we have another address configuration called fake_receive_level_2.py 

    address = {
        "inheritance":["fake_receive"],
        "message_type": "test_message_level_1",
        "carrier": "fake_message_listener_level_2",
        "$name": "$msg_type",
        "additional_info": {
            "topic": "ice_cream" 
        } 
    }

We can see that this address configuration inherits from the fake_receive address configuration. At runtime, all of fake_receive's field will be placed into this configuration. If there is a conflict where they have the same field, fake_receive_level_2's fields will override the inherited fields. 

So the runtime configuration would look like: 

    address = {
            "inheritance":["fake_receive"],
            "message_type": "test_message_level_1",
            "handler": "fake_message_handler",
            "handler_function": "process",
            "send_or_receive": "receive",
            "carrier": "fake_message_listener_level_2",
            "$name": "$msg_type",
            "duration": 10,
            "additional_info": {
                "topic": "ice_cream" 
            } 
        }

Inheritance is resolved left-to-right in the list. Inherited configs can inherit from other configs, which are resolved as they arise. Inherited dictionaries will update with new keys or override the same keys. 

## Keyword substitution 
There are three substiution keywords that can be handy to elimiate duplicate code in the configs. 

* __$name__: This replaces the key or value with the name of the config. 
* __$msg_type__: This replaces the key or value with the "message_type" indexed value relevant for the config (helpful for addresses)
* __$system_id__: Replaces the key or value with the system id value from the system config. This is often useful for a message or piece of information directly tied to the system instance 

These keywords **Do Not Inherit**. These are passed through to the configuration of interest. 

