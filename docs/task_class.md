## Tasks
Tasks are functionality within the system typically designed to keep system processes running smoothly. Examples of tasks include updating the system configurations, recovering data, checking fan temperature, and more. Tasks are similar to carriers in that they run with a specific trigger or duration. 


## Task Configuration

[For inheritance and keyword substitution, see this file](configuration_inheritance_and_keyword_substitution.md) 

Tasks are configured with task specific information that
will vary substantially by the particular carrier. 

However, at the very minimum, they need the following keys:

- "source" key with the name of the python file in the tasks source folder which contains the class which will implement the task code. **NOTE**: Sometimes, a task may used object code stored in a different folder (typically a carrier folder), especially if an infrequent operation needs to be run on a carrier. In this case, you would use the following keys:
    - "source_type": "carrier", (only supported other type at this time - CHECK)
    - "config_name": name of the config in that folder (ex: "mongodb_local")
- "function" key with the name of the function to be used in the class instance 
- "duration" (similar to address):  How often the message is sent through the system. This can be:
    - "always", if the task is always being run, 
    - a value in seconds, for how often the task is run (very typical), 
    - "on_message", for a task that runs on every new message coming through (also common), 
        - if the "on_message" duration is noted, the task config should also have a keyword "message_type" which denoted the type of message that triggers the task. 
    - "as_needed", if the send or received is triggered by something else on an as_needed basis 

Optionally, the configuration can have:
    - "arguments": a dictionary of function keyword/value pairs that will be passed to the function to be run 
    - any other task-specific information. 
    
For example, the task the checks the fans in the gateway is configured:

    {
        "source": "fan",
        "function": "fan_check",
        "arguments": {},
        "duration": 60,
        "fan_on_temp": 37.0,
        "fan_off_temp": 34.0,
        "power_pins": [18, 5]
    }

Meaning:
- a file named fan.py exists in the src/tasks folder which will implement this task class. 
- the function that will be run for the task is called "fan_check"
- no arguments will be passed to this function
- the task will run every 60 seconds
- "fan_on_temp", "fan_off_temp", and "power_pins" are task-specific configurable information for this task to use 

Alternatively, a carrier specific task called download_new_firmware_image.json is configured: 

    {
        "source_type": "carrier",
        "config_name": "s3_firmware_ota",
        "function": "handle_new_firmware_message",
        "arguments": {},
        "duration": "on_message",
        "message_type": "firmware_image" 
    }

Meaning:
- When the system receives a "firmware_image message", the task is triggered
- The carrier code file named "s3_firmware_ota" will run the task function, "handle_new_firmware_message". 
- This function takes no arguments, but in the task function (due to the on_message trigger) will have **message_type=None, entry_ids=[]** as keyword arguments


## Writing a New Task

All task class source should have the following functions:

init() - the initialization function, which takes in the configuration of the task as a keyword (config=). 

The tasks should also have the task function implemented that they will use to actually run the task:  

**NOTE**: If the task is triggered with "on_message", the function that implements that task MUST have the following keyword arguments in the function:
- message_type=None, 
- entry_ids=[]
which will allow the task function to pick up the appropriate message from the system. 


A specific task source code definition should include: 

* What durations, if any, a task can be defined with  

* Which arguments are necessary and which are optional in the config. Optional defaults if necessary. Kinds of values the arguments can take. 


At the most basic level, a task is a python class with 2 required functions: 

* an __init__ function, which is called when a new instance of the class is made 

* Whatever function implements the task. 

Outside of whatever the named task class is, there should be a return_object function that takes in the same init functions as the task and returns an instance of the task class. 

### The code file
The code file should have 
* imports, including (most likely) the import of the system object 
* The class stucture 
* Task specific function
* The return object function, returning an instance of the object 

### The imports
A developer will likely have their own code-specific imports, but most likely they will also be importing the system object to post and/or pickup messages. This import looks like: 

    #This line moves the system path up a directory 
    sys.path.append("../scarecro")
    import system_object


### The class structure 
The class can be named whatever you want in python. For example, the top level class declaration for the fan task looks like: 

    class Fan:

### The init function 
The init function for a task should likely have an optional config keyword: 

    def __init__(self, config={}):

which would allow the task to copy its configuration, if desired. 

The init() function of a task would typically store all its config variables in its own class variable for use by the task. 

For example, here is the init function for the Fan task: 

    def __init__(self, config={}):
        """
        Initializes the task with configuration provided 
        """
        self.config = config.copy()
        #Power pins - by default, 18 and 5 
        self.power_pins = self.config.get("power_pins", [18, 5])
        self.fan_on_temp = self.config.get("fan_on_temp", 37.0)
        self.fan_off_temp = self.config.get("fan_off_temp", 34.0)
        self.fans_running = False 
        self.temp_formatted = None

### Task Specific function
The task should have at least one function used in a task. For example, the fan_check function of the Fan class looks like this: 

    def fan_check(self):
            try:
                logging.info("Fan Check!")
                err, pi_temp = subprocess.getstatusoutput("vcgencmd measure_temp")
                temp = re.search(r'-?\d.?\d*', pi_temp)
                self.temp_formatted = float(temp.group())
                if self.temp_formatted >= self.fan_on_temp and self.fans_running == False:
                    self.turn_on_fans()
                elif self.temp_formatted <= self.fan_off_temp and self.fans_running == True:
                    self.turn_off_fans
            except Exception as e:
                logging.error(f"Could not perform fan check, {e}", exc_info=True)

### The return object function 
The return object funtion goes outside of the class definition, and takes in the same keyword arguments as the as init function for the class. This function simply returns the configured instance of the class. This function was implemented so the actual class code can be named according to programmers choice to improve readability. 

The example return_object function for the fan task is below: 

    def return_object(config):
    return Fan(config)

## Interfacing with the System
If the task has an on_message trigger, you will likely be picking up (and/or posting) messages to the system. Since tasks do not use addresses, you can use the system functions:
- pickup_messages_by_message_type(message_type=None, entry_ids=[])
- post_messages_by_type(messages, message_type)

TODO: More consistent naming scheme for pickup/post by type 

## Documenting a New Task 
If you create a new task, you need to document what configurations the task supports, including: 
- **Needed Task Configuration Info**: What information does the task implementation need in its own configuration? . 
- **Function to Run**: What function should the task run? 
- **Arguments**: Does the task function take any arguments. What are possible 
- **Durations**: What durations does the task support? If the task is run on message, what type of message?
- **Special Sourcing**: Does the task have a carrier source? If so, which one?  

We strongly encourage you to use a send function through a carrier rather than a task for most on_message queues, since send functions come with a notion of what messages to pickup. However, the same or similar scheme can be used by a task if necessary. 








