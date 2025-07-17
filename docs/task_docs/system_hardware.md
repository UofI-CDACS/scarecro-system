# Some Basic System Hardware Tasks
There are a couple of tasks implemented that perform some basic system hardware duties (namely for the solar-powered gateway) which are useful to have. These include
- checking whether or not the fan should be on
- patting the watchdog 

## Checking Whether or Not the Fan Should Be On 
### Source Code
/src/tasks/
**fan.py**

The fan.py file contains the function which implements the task here.

### Dependencies:
- Pigpio library installed on system 
TODO: Link how to do that 
- python libraries:
    - time
    - os
    - subprocess
    - sys

### Messages 
- no particular types of messages are needed for this task 


### Default Implementation 
#### Recommended Tasks and Ties to Source Code 

##### check_connection.json 

    {
        "source": "fan",
        "function": "fan_check",
        "arguments": {},
        "duration": 60,
        "fan_on_temp": 37.0,
        "fan_off_temp": 34.0,
        "power_pins": [18, 5]
    }

The fan task class expects the following arguments in the task config:

- "fan_on_temp": (Number), degree C of the processer at which to turn on the fan **Default**: 37.0
- "fan_off_temp": (Number): degree C of the processer at which to turn off the fan **Default**: 34.0
- "power_pins": (List of Numbers) power GPIO pins of fans to turn on/off **Default**: [18, 5] 


The fan_check function is meant to run on a numeric duration and does the following:
- checks the pi processor temp
- if it at or above the fan on temp
    - turn on the fan
- if it is at or below the fan off temp
    - turn off the fan 

#### Configurations Needed to Implement in the System:
**Gateway**:

Messages:
- None

Carriers:
- None

Addresses: 
- None 

Task Configs:
- fan_check 


**Data Store or Middle Agent**:
- Not really meant for these 


### Tests 
TODO: Describe these better
- TODO 


## Patting the Watchdog 
### Source Code
/src/tasks/
**watchdog.py**

The watchdog.py file contains the function which implements the task here.

### Dependencies:
- python libraries:
    - RPi.GPIO
    - time
    - logging

### Messages 
- no particular types of messages are needed for this task 


### Default Implementation 
#### Recommended Tasks and Ties to Source Code 

##### pat_watchdog.json 

    {
        "source": "watchdog",
        "function": "pat_the_dog",
        "arguments": {},
        "duration": 15,
        "pin": 4
    }

The watchdog task class expects the following arguments in the task config:

- "pin": (Number), pin number the watchdog timer is one **Default**: 4
 

The pat_the_dog function is meant to run on a numeric duration and does the following:
- turns on the watchdog pin as an output 
- sets it to False for 0.2 seconds
- sets the pin to True
- sets the pin back to an input  

#### Configurations Needed to Implement in the System:
**Gateway**:

Messages:
- None

Carriers:
- None

Addresses: 
- None 

Task Configs:
- pat_watchdog  


**Data Store or Middle Agent**:
- Not really meant for these 

### Tests 
TODO: Describe these better
- TODO 


