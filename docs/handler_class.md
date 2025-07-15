# Handlers Configurations
Handlers handle incoming and outgoing messages, including performing additional processing as necessary. Typically handlers work on some aspect of data translations, transformation, or cleaning. Sometimes, this is implemented in carrier, but for some classes of sensors, it makes more sense to break out in a handler file. 

Handlers are classes that deal with message content, including structuring, reorganizing, interpreting, or reorganizing message content. Handlers may not be necessary in all cases, especially if a message comes ready to use from a sensor. Handlers can be different on a incoming or outgoing message, or may only be used in one or the other. Handler functionality could be implemented entirely within a carrier, but it is often useful to separate this functionality, especially when working with multiple different brands of sensors using the same communication protocol (like several bluetooth sensors with different manufacturers). Handler configurations, should, at minimum, have a source field which indicates their source code class implementation. 

Why are handlers necessary? Sometimes you might have a group of sensors that use related interpration or cleaning functions which are useful to have decoupled from the actual sending/receiving procotols, especially if those protocols are shared with others types of sensors or data sources. 

## Configuring Handlers 

[For inheritance and keyword substitution, see this file](configuration_inheritance_and_keyword_substitution.md)

Handler configurations should at least the following keys:
- "source", pointing to the name of the python file implementing the particular task class (located in src/tasks). 

    {
        "source": name_of_task_class.py 
    }

For example, the handler for the renogy_solar_charger handler (renogy_solar_charger.json, located in configs/handlers) is configured:

    {
        "source": "renogy_solar_charger"
    }


## Writing a New Handler
A handler class needs the following:
* a class definition with an init function and one or more process functions 
* a return object function, similar to the carrier function with returns an instance of the handler class. 

### The init function 
The init function for the handler takes the following arguments
- **config**: The handler specific config dictionary
- **send_addresses**: A dictionary of send function addresses, the same as for carriers
- **receive_addresses**: A dictionary of receive addresses, the same as for carriers
- **message_configs**: A dictionary of message configurations, the same as for carriers. 

The handler may or may not need to use this information. 

### One or more process functions. 
Each process function can be named anything, but will receive two arguments:
- **message_type**: The type of message
- **messages**: A list of messages to process 

The function may or may not use the addresses to tie processing information together. 

The processing functions should return a list of processed messages. 

### Return object function
This follow this same format as for carriers. For example, for the KKM_K6P handler, it looks like: 

    def return_object(config={}, send_addresses={}, receive_addresses={}, message_configs={}):
        return KKM_K6P(config=config, send_addresses=send_addresses, receive_addresses=receive_addresses, message_configs=message_configs)

### Documenting a New Handler 
Handler documentation should include: 
* What init information should be included in the specific handler initialization.
* What address-specific information should be included in the address, if any. 
* What functions can be used as processing functions and the circumstances each should be used in. Include any envelope overrides, if necessary. 


