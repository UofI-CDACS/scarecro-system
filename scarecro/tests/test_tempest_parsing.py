import sys
import time 
import json 
sys.path.append("../scarecro")
import logging 
import system_object
#Get the system config
import src.system.system as system_class 
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s - %(asctime)s - %(message)s')
#logging.Formatter('%(levelname)s - %(asctime)s - %(message)s')

forecast_msg = {
    #too much proprietary info in message 
}
enveloped_message = {
            "msg_id": "test_device",
            "msg_time": "now",
            "msg_type": "tempest_forecast",
            "msg_content": forecast_msg
            }


system_config = {
    "id": "test_device",
    "addresses": [
        "tempest_forecast_in"
    ],

}

#Init the 
system_object.system = system_class.return_object(system_config=system_config)
system_object.system.init_ecosystem()
system_object.system.start_scheduler()
#Print system update variable 
print("Before tempest message sent")
time.sleep(2)
system_object.system.post_messages(enveloped_message, "tempest_forecast_in")


while True:
    time.sleep(15)
    pass 

