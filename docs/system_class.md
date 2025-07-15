# System Class 

## Purpose of the System Class
The system class is effectively the control scheme for the entire SCARECR system. It handles all of the information routing and interim storage. The system class is initialized with a system configuration. In general, to run a scarecro system, you:
- initialize the system class with the system configuration 
- initialize the system ecosystem with the init_ecosystem() function
- start the system schedule with the start_scheduler() function
- sleep.
Note that since the system class hosts most of the control of SCARECRO, is is a **hefty** code file size. It is not recommended to make changes to this file unless you are confident in your development choices. 

## System Configuration
The system config should have the following fields:

id: The id of this particular system device 

addresses: 
    A list of address configuration names that are in play for the system. These names should correspond to the names of json files in the configs/addresses folder. 

tasks:
    A list of task configuration names that are in place for the system. These names should correspond to the names of json files in the configs/tasks folder.

## System Class Responsibilities 
The system class is the main "brain" of the SCARECRO system. It is responsible for:
* Initializing itself with the proper functionality it is configured for. This includes:
    * Ensuring proper inheritance on all configurations
    * Ensuring keyword substitution on all configurations
    * Ensuring source code exists for all configurations  
* Scheduling all system behavior, including:
    * All carrier sending/receiving functions, at the proper duration, or linked to the proper trigger
    * All tasks the system must run 
    * And tying handler functions to incoming or outgoing messages


## System Internal Variables - Message Table for Stored State Messages
Messages Received by the System are stored in state as a "message table" which is actually a dictionary of this format:   

    message_type: 
                {
                    {
                    "latest_entry_id": 0,
                    "semaphore": threading.Semaphore(),
                    "messages": {
                        msg_id: {<enveloped message>}
                        msg_id: {<enveloped message>}
                        }
                    }
                }

For example, let's say we receive ave the following messages: 

- A message from a weather rack sensor with ID 21 (received first)
- A message from weather rack sensors with ID 39 (received second)
- A message from bmp280 sensor with ID 301 (received third)

The dictionary in the system state would look like this 

    {
        weather_rack: {
            "latest_entry_id": 1
            "semaphore": <semaphore_object_000>,
            "messages": {
                21: {
                    "entry_id": 0
                    "msg_id": 21, 
                    "msg_time": "2024-05-16T00:00:00.000000",
                    "msg_type": "weather_rack"
                    "msg_content": {
                        "temperature": 60
                        ...
                    }
                    ...
                },
                39: {
                    "entry_id": 1
                    "msg_id": 39, 
                    "msg_time": "2024-05-16T00:05:00.000000",
                    "msg_type": "weather_rack" 
                    "msg_content": {
                        "temperature": 43
                        ...
                    }
                    ...
                },

            }
        "bmp280": {
            "latest_entry_id": 0,
            "semaphore":  <semaphore_object_001>,
            "messages": {
                "301": 
                {
                    "entry_id": 0
                    "msg_id": 301, 
                    "msg_time": "2024-05-16T00:15:00.000000"
                    "msg_type": "bmp280" 
                    "msg_content": {
                        "pressure": 52
                        ...
                }
            }
    }

Which basically corresponds to a table that would look like this: 

| Message Type | Message ID | Entry ID | Message Content | 
| ------------ | ---------- | -------- | -------- | 
| weather_rack |     21     |  0  | {temperature: 60,...} |
| weather_rack |    39      |  1  |  {temperature: 43,...}|
| bmp280       |    301     |  0  | {pressure: 52, ...} | 

If we get a new weather rack message from ID 21, with a new reading, the underlying dictionary would update: 

    {
        weather_rack: {
            "latest_entry_id": 2
            "semaphore": <semaphore_object_000>,
            "messages": {
                21: {
                    "entry_id": 2
                    "msg_id": 21, 
                    "msg_time": "2024-05-16T00:00:00.000000",
                    "msg_type": "weather_rack"
                    "msg_content": {
                        "temperature": 56
                        ...
                    }
                    ...
                },
                39: {
                    "entry_id": 1
                    "msg_id": 39, 
                    "msg_time": "2024-05-16T00:05:00.000000",
                    "msg_type": "weather_rack" 
                    "msg_content": {
                        "temperature": 43
                        ...
                    }
                    ...
                },

            }
        "bmp280": {
            "latest_entry_id": 0,
            "semaphore":  <semaphore_object_001>,
            "messages": {
                "301": 
                {
                    "entry_id": 0
                    "msg_id": 301, 
                    "msg_time": "2024-05-16T00:15:00.000000"
                    "msg_type": "bmp280" 
                    "msg_content": {
                        "pressure": 52
                        ...
                }
            }
    }

And this would correspond to a message table that looks like: 
| Message Type | Message ID | Entry ID | Message Content | 
| ------------ | ---------- | -------- | -------- | 
| weather_rack |     21     |  2  | {temperature: 56,...} |
| weather_rack |    39      |  1  |  {temperature: 43,...}|
| bmp280       |    301     |  0  | {pressure: 52, ...} |

You can see that only the latest message from each possible sender (indicated by the message id) is kept by the system in order to avoid massive memory bloat. If message histories need to be kept, the maintainers would recommend utilizing a database carrier trigged on message receipt, or else implementing this functionality in a handler or carrier. 

## System Behavior 

### Initializing the system class 

The system class expects a system configuration dictionary to be located in configs/system in a file called system.json, which contains one json dictionary following the config format noted prior. However, this expectation can be overriden by passing the system a custom system configuration dictionary, which it will use instead. 

The init() function copies over the system configuration, sets the system id, and a connection and updater variable. 

### Initilizing the system ecosystem 
When the init_ecosystem() function is called, the system will do the following: 

1. Initialize all the "post office" configurations: 
 -  **Grab all the address configs** from those listed in the system configs. The system will try and resolve inheritahance and substitutions in the address configs at this step. 
- **Grab all the message configs**, related to the active addresses. The system will try and resolve all inheritance and substitution in the message configs at this step. 
- **Get all the handler configs**, related to the active addresses. The system will try and resolve all inheritance and substitution in the handler configs at this step. 
- **Grab all the carrier configs**, related to the active addresses. The system will try and resolve all inheritance and substitution in the carrier configs at this step. 
- **Grab all task configs**, indicated as active in the system configuration. 

2. **Create a message table**: This system will create an internal message table, with a new entry for each configured message in the system. This new entry for each message is a dictionary with the latest_entry_id field defaulting to 0, a new semaphore class specific to that message type, and a "messages" field linked to an empty dictionary. 

7. **Instantiate the handler classes**: The system will create a new handler class instance from indicated source code based on the active handler instance configurations. This will be stored in the system handler dict (self.handlers) indexed by the handler name.  

8. **Instantiate the carrier classes**: The system will create a new carrier from the indicated source code based  on the active carrier class instance configurations. This will be stored in the system carrier dict (self.carriers) indexed by the carrier name. 

9. **Instantiate the task classes**: The system will create a new task class instance from the indicated source code based on the active task class configurations. These will be stored in the system task dict (self.tasks) indexed by the task name. 

10. **Initialize the updater code**., if one is set. TODO: Fill in more 

11. **Initialize a scheduler**: The system will create a new python APScheduler scheduler (self.scheduler) to handle threading tasks. By default, there is a maximum of 50 thread workers in the scheduler. 

12. **Initialize the scheduler**: The system will create a a scheduler (using APSscheduler) and then an initialization dictionary for scheduled system tasks based on the active addresses and tasks. It will then schedule all the jobs in the system. 

### Starting the System Scheduler 
Calling (TODO: Start scheduler or start system??) 
will beging the scheduler, which will run APScheduling background threads to handle all system behavior 

## Underlying system storage of Classes and Configurations 

**Addresses**: 
A dictionary stored in self.addresses of the form: 

    {
        "address_name": address configuration
    }

For example: 

    {
        "datagator_mqtt_in": {
            "inheritance": [],
            "message_type": "datagator",
            "handler": "datagator",
            "handler_function": "process",
            "send_or_receive": "receive",
            "carrier": "mqtt_sensor_listener",
            "duration": "always",
            "additional_info": {
                "topic": "datagator"
            }
        },
        "datagator_mqtt_out": {
            "inheritance": [],
            "message_type": "datagator",
            "handler": "datagator",
            "handler_function": "process",
            "send_or_receive": "send",
            "carrier": "mqtt_sensor_listener",
            "duration": 10,
            "additional_info": {
                "topic": "datagator_2"
            }
        }
    }

**Messages**: 
A dictionary stored in the variable self.messages of the form: 

    {
        "message_name": {
            "addresses": [list of addresses that use the message],
            "content": message config,
        }
    }

For example: 

    {
        "datagator": {
            "addresses": [
                "datagator_mqtt_in",
                "datagator_mqtt_out"
            ],
            "content": {
                "inheritance": [],
                "id_field": "id",
                "time_field": "time"
            }
        }
    }

**Handlers**: A dictionary stored in self.handlers variables of the form: 

    {
        "handler_name": {
            "addresses": [list of addresses that use this handler],
            "content": handler config, 
            "object": reference to actual class instance of handler instantiation 
        }  
    }

For example: 

    {
        "datagator": {
            "addresses": [
                "datagator_mqtt_in",
                "datagator_mqtt_out"
            ],
            "content": {
                "source": "datagator"
            },
            "object": "<src.handlers.datagator.DataGator object at 0x7f4982dd3940>"
        }
    }

**Carriers**:

A dictionary stored in the self.carriers variable of the form: 

    {
        "carrier_name": {
            "addresses": [list of addresses that use this carrier],
            "content": carrier config, 
            "object": reference to actual class instance of carrier instantiation 
        }  
    }

For example: 

    {
        "mqtt_sensor_listener": {
            "addresses": [
                "datagator_mqtt_in",
                "datagator_mqtt_out"
            ],
            "content": {
                "source": "mqtt",
                "mqtt_url": "some_url.hivemq.cloud",
                "mqtt_port": 1883,
                "mqtt_username": "user",
                "mqtt_password": "1234",
                "qos": 1,
                "client_id": "sensor_listener"
            },
            "object": "<src.carriers.mqtt.MQTT_Client object at 0x7f49807a3208>"
        }
    }


__Tasks__: 
A dictionary stored in the self.tasks variable of the form: 

    {
        "task_name": task config
    }

For example: 

{
    "fake_print_often": {
        "source": "fake_task_options",
        "function": "obnoxious_print",
        "arguments": {},
        "duration": 8,
        "object": "<src.tasks.fake_task_options.FakeTasks object at 0x7f4dd5d06ac8>"
    }
}

### Scheduling functions and tasks 
In order to schedule system functionality correctly, the system needs to understand what functions need to be run when. So, the system creates a dictionary for the scheduler with the following form: 

    {
        "job_id":
        {
            "object_name": name of the configured class instance  in the system
            "object": Reference to class instance that runs the function
            "job_id": Unique id of the job
            "function": function to run
            "arguments": arguments the pass to the function, in a list
            "duration": How often the job should be run in seconds, or "always"
            "type": "task" or "carrier", depending on which it is
        }
    }

This object is stored in **self.scheduler_dict**. During this process, however, it creates another important dictionary that tracks which of these jobs should be executed not by the scheduler, but by an on_message event. This dictionary looks like: 

    {
        "message_type": [job_id_1, job_id_2,...]
    }

Where each message type in the dictionary has a list of associated job ids that should execute if a message of that type is received. This is stored in **self.on_message_routing_dict**. 

The above dictionaries are created based on the durations configured in both the addresses and the tasks configurations. 

After the **scheduler_dict** object is created, the jobs can be scheduled with the scheduler. Jobs with a numeric duration or a duration equal to "always" are scheduled with the scheduler. Jobs with a duration that doesn't fit these categories are not scheduled. Carriers and tasks are scheduled nearly the same way, except carrier class functions expect the duration value, which is appended to their arguments field of the job scheduling. 


### Interacting with the System  Object 
- importing the system class instance 
- enveloping messages
- posting/picking up messages from the system message table 
- getting the system id 

#### Importing the System Class Instance

For carrier to use the system class instance, the carrier needs to import the system object: 

    import system_object 


Then the carrier will need to reference the functions on the system attribute of the system object, like:

    system_object.system.pickup_messages(address_name)

### Enveloping the Message

To envelope the message, the carrier or task can either implement the enveloping format around the message themselves, or they can use the envelope_message function of the system class instance. The __envelope_message__ function takes two arguments:

1. The raw message (in a dictionary format)
2. The address associated with the message 

This function uses the message field information to try and envelope the message. However, any envelope information can be overriden by the handler, which is often useful if the raw data is not in the correct format yet or if the message keeps track of the reading time separately from the system receipt. 

The envelope_message function:
* Uses the message id_field information to get the message id
* Uses the current time in UTC to populate the time field
* Uses the message type from the address to populate the message type field
* Puts the passed message into the "msg_content" field 

Example enveloped message: 

    {
        'msg_id': '1', 
        'msg_time': 'now', 
        'msg_type': 
        'test_message', 
        'msg_content': 
            {
                'id': '1', 
                'time': 'now', 
                'place': 'here', 
                'who': 'me',
                'processed_by_fake_message_handler': True
            }, 
        'entry_id': 1}
    } 

Where the raw message was: 

    {
        'id': '1', 
        'time': 'now', 
        'place': 'here', 
        'who': 'me',
        'processed_by_fake_message_handler': True
    }



### Posting Messages to the Message Table 
Carriers (see Writing a New Carrier) should have at minimum, a receive or send function. If the carrier is written to receive messages, at some point in the receive function (or in a sub-function executed by the receive function), the carrier should at some point use the __post_messages__ function of the system class instance to drop the messages off at the post office. The function takes two arguments:

1. The message (or list of messages), in enveloped format,
2. The name of the address the message is being sent on 

When the enveloped message(s) is/are posted along with the address via the "post_messages" function, the following occurs:

* All messages are run through their configured handler, if they have one. The handler may make changes to the time field or id field, depending on how it parses content 
* The message is added to the message table in the system. This "stamps" the message, added the "latest_entry_id" field to the envelope structure. The latest entry id is also updated in the internal message table structure. 
* The message is checked for any "on_message" triggers that need to be executed if that particular message is received. Those triggers are then executed. 

There are some cases where you may not use the address. In this case, you can use the 
**post_messages_by_type** function, which takes in the enveloped messages and message type.

### Picking Up Messages from the Message Table 
The carrier or task picks up post office messages via the
**pickup_messages** function. This function takes in the address name, and can optionally take in a keyword argument of **entry_ids**. The entry_ids are a list of entry ids in the message table (and in the stamped message envelope). This is a useful argument for on_message carrier triggers, as it allows them to only pick up the new message. When this keyword is not supplied, all messages corresponding to the address are picked up and returned as a list. 

In a case where the address is not relevant, use **pickup_messages_by_type** function, where the message_type keyword is set to the message type. 


**NOTE: Posting and picking up messages are semaphore-protected operations to prevent race conditions throughout various parts of the system.**

### Getting the system id
Some code functionality may need the system id. That can be gained from the system using the **return_system_id** function which takes no arguments and returns the id of the system. 

TODO: Visuals 
TODO: Add system config examples 