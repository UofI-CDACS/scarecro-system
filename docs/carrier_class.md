# Carrier Class

Carriers send and receive messages. There analogous component in the post office illustration could be a mail car, a mail truck, a door-to-door mail carrier, or even a mail plane. Carrier configurations should have, at minimum, a source field indicating the source code implementation of the carrier.

## Carrier Configuration

[For inheritance and keyword substitution, see this file](configuration_inheritance_and_keyword_substitution.md) 

Carriers are configured with carrier specific information that
will vary substantially by the particular carrier. 

However, at the very minimum, they need a "source" key with the name of the python file in the carriers source folder which contains the class which will implement the carrier code. 

    {
        "source": python source code file name where the carrier will be implemented. 
    }

For example, the 433_Radio Carrier config stored in the 433_listener.json file we use has this simple configuration:

    {
        "source": "433_radio"
    }

Meaning a file named 433_radio.py exists in the src/carriers folder which will implement this carrier class. 


All carrier object source code classes should have the following functions:

init() - the initialization function, which takes in the configuration of the carrier as well as all addresses that use the carrier, and message definitons that use the addresses 

And, depending on functionality, have one or more of these functions:  

send() - a function that takes in a list of addresses, the duration, (and an optional list of entry ids), grabs the messages corresponding to those addresses (optionally filtered by entry id), and sends them. 

receive() - a function that takes in the address(es) names, duration, and is able to recieve the message(s) and package it before placing into the message table.


A specific carrier source code definition should include: 

* What durations, if any, a send/receive function is defined with 

* Which arguments are necessary and which are optional in the config. Optional defaults if necessary. Kinds of values the arguments can take 

* what form of message the carrier passes 
to the handler 


## Writing a New Carrier

At the most basic level, a carrier is a python class with 2 required functions: 

* an __init__ function, which is called when a new instance of the class is made 

* Either a __send__ function, or a __receive__ function, or both, depending on what the carrier class is capable of. 

Outside of whatever the named carrier class is, there should be a return_object function that takes in the same init functions as the carrier (described later) and returns an instance of the carrier class. 

### The code file
The code file should have 
* imports, including (most likely) the import of the system object 
* The class stucture 
* The return object function, returning an instance of the object 

### The imports
A developer will likely have their own code-specific imports, but most likely they will also be importing the system object to post and/or pickup messages. This import looks like: 

    #This line moves the system path up a directory 
    sys.path.append("../scarecro")
    import system_object


### The class structure 
The class can be named whatever you want in python. For example, the top level class declaration for the 433 MHz carrier looks like: 

    class Radio_433():

### The init function 
The init function for a carrier will always take in 4 arguments, which are passed in by the system: 

    def __init__(self, config, send_addresses, receive_addresses, message_configs):

These 4 arguments are:

- **config**: The configuration for the carrier, passed in as the configuration dictionary 
- **send_addresses**: A dictionary of addresses that this carrier should be sending messages on, or an empty dictionary if there are no addresses for this function. This dictionary takes the form:

        {
            address_name: address_config 
        }

- **receive addresses**: A dictionary of addresses that this carrier should be receiving messages on, or an empty dictionary if there are no addresses for this function. This dictionary also takes the form: 

        {
            address_name: address_config 
        } 

- **message_configs**: A dicionary of message configs indexed by message name. This contains all messages used by either send or receive addresses. It takes the form: 

        {
            message_type: message_config 
        }

The init() function of a carrier would typically store all these variables in its own class variable for use by the carrier. As a **tip**, most carriers also want to make some sort of address mapping lookup table based on the messages they receive or send. This mapping information is usually defined somewhere in the address config, and allows the carrier to somehow tie the messages it receives on whatever protocol it uses to a specific address. 

For example, here is the init function for the 433 MHz carrier: 

    def __init__(self, config, send_addresses, receive_addresses, message_configs):
            """
            This driver doesn't really need anything configuration-wise
            String matches and drivers are provided on an address level 
            """
            self.config = config.copy()
            self.send_addresses = send_addresses.copy()
            self.receive_addresses = receive_addresses.copy()
            self.message_configs = message_configs.copy()
            self.create_mappings()
            self.cmd = ['/usr/local/bin/rtl_433', '-q', '-M', 'level', '-F', 'json']

You can see that the actual carrier config doesn't contain a lot of info for this carrier. Often, for a carrier, the carrier config will contain remote connection info like a username/password. 

However, the carrier init function copies all the init arguments to its own class variables. It also has a subprocess command it uses as a class variable. In it's init function, it runs a create_mappings() function will ties the string match information provided on the address level to info it will receive in it's SDR stream. The create_mappings() function looks like: 

    def create_mappings(self):
            matches_address_mapping = {}
            address_matches_mapping = {}
            driver_address_mapping = {}
            address_driver_mapping = {}

            all_addresses = {**self.send_addresses, **self.receive_addresses}
            for address_name, address_config in all_addresses.items():
                add_info = address_config.get("additional_info", {})
                string_matches = add_info.get("string_matches", [])
                driver = add_info.get("driver", None)
                driver_address_mapping[driver] = address_name
                address_driver_mapping[address_name] = driver
                for match in string_matches:
                    matches_address_mapping[match] = address_name
                address_matches_mapping[address_name] = string_matches
            self.matches_address_mapping = matches_address_mapping
            self.address_matches_mapping = address_matches_mapping
            self.driver_address_mapping = driver_address_mapping
            self.address_driver_mapping = address_driver_mapping

In the additional_info section of the address, this carrier expects a "string_matches" field which allows it to tie this address to stream information. It creates these ties from address to string match and from string match to address. It also matches the "driver" field of the address to the driver command argument it will need to use when initializing the SDR listen stream. 

### The recieve function 
The receive function takes in 2 arguments:
- **address_names**: A list of address names that should be active for the receive function. This may be a subset, but never a superset, of the receive addresses the carrier received during the initalization. The reason this may be a subset is because the same connection object might handle different message receipts at different times. 
- **duration**: The duration of the receive, most likely a numeric number of seconds or the word "always". 
The scheduler is using the duration for a carrier to decide how often to run the function. **If the duration is "always", the function should never return for normal behavior**. The scheduler will run the function with the expectation that the function won't return. If the duration is a number of seconds, **the carrier will run the function every time that number of seconds elapses**. It will **NOT** run that function for that number of seconds - it expects the function to run and then return. It is up to the carrier implementer to decide how to long to wait, if any time at all, for receiving messages when the duration is not "always". The implementer could also decide to make this a configurable value. 

Somewhere in the receive function, the carrier should have the ability to receive messages, tie them to addresses, and post them to the post office. 

Here is the receive function for the 433 MHz carrier: 

    def receive(self, address_names, duration):
            """
            Takes in the address names and the duration
            For this driver, the duration will pretty much always be 'always'
            You could potentally define other behavior, like listening 
            for a set amount of time.  
            """
            cmd = self.make_command(address_names)
            self.connect(cmd)
            self.time_since_last_sample = time.time() - self.last_sample_received
            if duration == "always":
                while True:
                    self.time_since_last_sample = time.time() - self.last_sample_received
                    self.listen()
            else:
                try:
                    prev_time = time.time()
                    curr_time = time.time()
                    time_out = curr_time-prev_time
                    #Heuristic - could have this configured 
                    while time_out < 20.0:
                        self.listen()
                        curr_time = time.time()
                        time_out = curr_time-prev_time
                    self.disconnect()
                except Exception as e:
                    logging.error(f"Could not listen on for period of time on 433 {e}")
                
You can see this function has the ability to make a driver command based on the active addresses it receives. It then decides to run a listen function either a forever loop or a timeout loop. The listen function (and nested functions) handle the message mapping and posting. 

### The send function 
The send function operates the same way as the receive function, except it has an additional optional keyword argument, **entry_ids**. This argument, if used, expects a list of entry_ids from the system message table, which has the send function send ONLY those entry ids. 

The send function would use the **pickup_messages** function from the system to get a list of messages to send. It then sends messages based on the carrier implementation. 

For example, here is the send function for the mqtt carrier: 

    def send(self, address_names, duration, entry_ids=[]):
            """
            High level exposure function of the carrier
            Takes in an optional list of entry ids
            Grabs the messages and publishes them, optionally filtering by ID 
            No "always" duration is really defined for this driver, don't use with always 
            """
            for address_name in address_names:
                try:
                    #Look up the topic
                    topic = self.address_topic_mapping.get(address_name, None)
                    if topic:
                        #Get the messages
                        messages = system_object.system.pickup_messages(address_name, entry_ids=entry_ids)
                        new_entry_ids = []
                        sent_entries = self.sent_entries.get(topic, [])
                        #Send each message individually 
                        if messages != []:
                            self.connect(reconnect=False)
                            self.run(duration=duration)
                        for message in messages:
                            entry_id = message.get("entry_id", None)
                            new_entry_ids.append(entry_id)
                            
                            #Send only if we haven't already sent it
                            if entry_id not in sent_entries:
                                content = message.get("msg_content", {})
                                return_val = self.publish(topic, content)
                        self.sent_entries[topic] = new_entry_ids
                except Exception as e:
                    logging.error(f"Could not publish message on address {address_name}", exc_info=True)
        
It can be seen that this function gets the topic mapping for each address it is passed. It picks up the messages for that address, grabs the entry id, and if it hasn't already sent the message corresponding the entry id, it sends it on the topic. 

### The return object function 
The return object funtion goes outside of the class definition, and takes in the same keyword arguments as the as init function for the class. This function simply returns the configured instance of the class. This function was implemented so the actual class code can be named according to programmers choice to improve readability. 

The example return_object function for the mqtt carrier is below: 

    def return_object(config={}, send_addresses={}, receive_addresses={}, message_configs={}):
        return MQTT_Client(config=config, send_addresses=send_addresses, receive_addresses=receive_addresses, message_configs=message_configs)


### Documenting a New Carrier 
If you create a new carrier, you need to document what configurations the carrier supports, including
- **Needed Carrier Configuration Info**: What information does the carrier implementation need in its own configuration? This could include something like a connection string, a username/password, or even a GPIO pin. 
- **Send/Receive and Durations**: Does the carrier support sending or receiving or both? What duration types does it support for each function (send/receive)
- **Address Configurations**: What information, if any, does an address need to include in its "additional_info" section to tie a message the carrier receives to a specific address, or to listen on that address in the first place? For example, for an mqtt carrier, this might be the sensor-specific mqtt topic. For a database carrier, this might be the database table name the address is tied to.  