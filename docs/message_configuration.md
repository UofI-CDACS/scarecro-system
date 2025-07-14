# Messages 

Any type of message packet send through the SCARECRO system must have a message configuration attached to it in order for it to be routed and parsed effectively. Message configurations live

## Message Configuration  
Message configurations are located here: 
- scarecro 
    - configs
        - messages  
            - default_sensor.json
            - etc... 

A message configuration should be a json file containing a  dictionary with the following form: 

    {

        "id_field": The identification field of the message content. This will usually identify the unique device sending it, but may be another way of identifying distinct messages. 

        "time_field": The field of the message the identifies where the time of message generation/receipt is located. 

        "inheritance": A string or list of string of messages this message inherits from. If the message inherits from a message which already has the id_field or time_field implemented, it would not need to implement the fields itself. 

    }

One message configuration that comes with the system by default is **default_sensor.json**. This json file contains the dictionary:

    {
        "id_field": "id",
        "time_field": "time"
    }

Which indicates that the message will have a field in it called "id", which contains the unique identifier of the message sender/generator, and a field called "time", which will contain the timestamp of the message. 

TODO: If a message config isn't present, it should maybe default to the name plus the inheritance of the default sensor. May cause some typo issues however - research. 

## Messages in the system object 
Messages exchanged by the system between processes will be packaged in the following format:
    
    {
        "msg_id": message_id (using the id field),
        "msg_time": either time of receipt or timestamp of message, if time field is implemented,
        "msg_type": message_type (linked to the name of the message config ),
        "msg_content": the actual message packet 
    } 

When messages are added to a message table by the system, the system also tracks the latest **entry_id** as a field to help with eliminating duplicate sending and to track the latest message per unique sending device. 

Therefore, a message in the overall system table will look like:

    {
        "msg_id": message_id (using the id field),
        "msg_time": either time of receipt or timestamp of message, if time field is implemented,
        "msg_type": message_type (linked to the name of the message config ),
        "msg_content": the actual message packet 
        "entry_id": unique, ordered identifier allowing the message table to understand the latest message entry for a given message type or id 
    } 

There are two helper functions from the **system** object (system source code file) that help carrier functions (or anything other code files dealing with messages) put messages in this format. They are: 

- envelope_message(message_content, address_name): takes the message packet and the name of the address it came on, and uses the message definition (from the address) to create the enveloped message (see system object for defaults), 
- envelope_message_by_type(message_content, message_type): takes the message packet and the message type directly and uses the message definition to create the enveloped message
TODO: Add explanation over why you might use one over the other 
## See Also:
TODO 



