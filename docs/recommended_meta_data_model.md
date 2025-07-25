# Recommended Meta Data Model  

SCARECRO operates on a data model for configuring carriers, messages, handlers, addresses, and tasks. However except of the limitation of being json-formatted and have some sort of id and time field, the SCARECRO system is fairly agnostic to the format of the messages themselves. When it comes to analyzing and visualizing data, however, it is useful to have a **meta_data_model** to keep track of the format and storage of data throughout the system. In our deployments, we will be keeing track of data using two concepts: data source **messages** and data source **instances**, using three separate json schemas. 

## Messages
Messages are the sensor readings and system updates sent throughout the system, the physically packaged data for the system users. We have created a json schema for messages that gives information about the message itself and uses an additional **fields** schema to describe the fields of the message. 

### Message Schema
This is also located in [examples/schemas/message_schema.json](../scarecro/examples/schemas/message_schema.json)

    {
        "type": "object",
        "title": "message",
        "properties": {
            "message_id": {
                "type": "string",
                "description": "Unique id of the message type - often the message name"
            },
            "display_name":{
                "type": "string",
                "description": "display name of the message"
            },
            "instance_database":{
                "type": "string",
                "description": "Instance collection or table storage location for this message type"
            },
            "message_database":{
                "type": "string",
                "description": "Messages collection or table storage location for this message type"
            },
            "id_field":{
                "type": "string",
                "description": "field name that stores the unique identifier for the message reporter instance"
            },
            "time_field":{
                "type": "string",
                "description": "field name that stores the timestamp for the message, if it exists"
            },
            "timestamp_field_format":{
                "type": "string",
                "description": "format of the message timestamp"
            },
            "timezone":{
                "type": "string",
                "description": "message timezone, if known"
            },
            "message_rate":{
                "type": "number",
                "description": "approximate average reporting rate of message per instance, in seconds, if known"
            },
            "map_icon": {
                "type": "string",
                "description": "map icon for this message type"
            },
            "tags":{
                "type": "array",
                "items": {"type": "string"}
            },
            "inheritance":{
                "type": "array",
                "items": {"type": "string"},
                "description": "list of message IDs this message inherits from"
            },
            "description": {
                "type": "string",
                "description": "Optional description of the message type"
            },
            "fields": {
                "type": "array",
                "items": {"type": "object"},
                "description": "list of field objects the message contains"
            }
        },
        "required": ["message_id"]
    }


The **message_id** is usually the name of the message. The id_field and time_field directly translate from the message config, and the message schema is designed so that it can be interchangebaly with message configs, if desired. 

The **fields** key, in our system, expects the objects to conform to the field schema. 

### Field Schema 

This is also located in [examples/schemas/field_schema.json](../scarecro/examples/schemas/field_schema.json)


    {
        "type": "object",
        "title": "field",
        "properties": {
            "field_name": {
                "type": "string",
                "description": "Name of the field"
            },
            "display_name":{
                "type": "string",
                "description": "display name of the field"
            },
            "data_type":{
                "type": "string",
                "description": "data type of the field - can be string, number, boolean, date, or unknown",
                "enum": ["string", "number", "boolean","object", "array", "date", "unknown"]
            },
            "kind":{
                "type": "string",
                "description": "notes whether the field is reported, calculated, or unknown",
                "enum": ["reported", "calculated", "unknown"]
            },
            "units":{
                "type": "string",
                "description": "Units of the field, if known and applicable"
            },
            "tags":{
                "type": "array",
                "items": {"type": "string"}
            },
            "description": {
                "type": "string",
                "description": "Optional description of the field"
            }
        },
        "required": ["field_name"]
    }

The only required key is the **field_name**. 

## Instances 
Instances are specific generators of data, most often used to identify individual sensors, system components, or locations. 

The instance schema is below and can also be found in This is also located in [examples/schemas/instance_schema.json](../scarecro/examples/schemas/instance_schema.json)

    {
        "type": "object",
        "title": "instance",
        "properties": {
            "instance_id": {
                "type": ["string","number"],
                "description": "Unique id of the instance"
            },
            "display_name":{
                "type": "string",
                "description": "display name of the instance"
            },
            "message_type":{
                "type": "string",
                "description": "associated message type of the instance - should map to a message id"
            },
            "latitude":{
                "type": "number",
                "description": "Latitude coordinate of the instance"
            },
            "longitude":{
                "type": "number",
                "description": "Longitude coordinate of the instance"
            },
            "altitude_orthometric":{
                "type": "number",
                "description": "Orthometric altitude of the instance"
            },
            "tags":{
                "type": "array",
                "items": {"type": "string"}
            },
            "description": {
                "type": "string",
                "description": "Optional description of the instance"
            }
        },
        "required": ["instance_id"]
    }

The only required field is **instance_id**, which would be expected to have a value that matched a value in the messages **id_field** in deployment. 


## Tag Schema
It can be useful to mark different messages and instances with resuable tags for downstream filtering (hence why messages, instances, and fields have an optional tag field). To this end, we also created a tag schema (mappable to the tag name fields) to aid with this. The schema is below and also can be found in [examples/schemas/tag_schema.json](../scarecro/examples/schemas/tag_schema.json)



    {
        "type": "object",
        "title": "tag",
        "properties": {
            "tag_id": {
                "type": "string",
                "description": "unique identifier for a given tag"
            },
            "display_name":{
                "type": "string",
                "description": "display name of the tag"
            },
            "description":{
                "type": "string",
                "description": "description of the tag"
            }
        },
        "required": ["tag_id"]
    }

The only required field is **tag_id**. 

## Implementation 
In our test system, we have collection named **messages** where all our meta data message definitions (used also as the configs) live. 
 
Our meta data instances live in collections named {message_type}_instances. 

## Examples and Verifying Schemas 

You can see some example messages that conform to the meta-data message schema (and message configuration) in [/examples/example_messages/](../scarecro/examples/example_messages/)

You can see some example instances (where you need to fill in missing information) in [/examples/example_instances/](../scarecro/examples/example_instances/)


You can test some schema verification (and create and test your own messages and instances) with the scripts located in **/examples/**

- [verify_message_schema](../scarecro/examples/verify_message_schema.py)
- [verify_instance_schema](../scarecro/examples/verify_instance_schema.py)


