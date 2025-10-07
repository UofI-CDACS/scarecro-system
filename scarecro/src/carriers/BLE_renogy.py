import sys
import time 
import logging 
import json 
import os 
from threading import Timer
import libscrc
import gatt
sys.path.append("../scarecro")
import system_object
import util.util as util 

#Licensing:
#This code is generated from: https://github.com/cyrils/renogy-bt 
#It has been modified to fit this use case. 


class BLE_renogy():
    def __init__(self, config, send_addresses, receive_addresses, message_configs):
        """
        Bluetooth needs to know on config level:
        1.The method of connection - beacon or write_read?
        2.listening_interval (default)

        On address level needs to know: 
        1. uuid of data to read 
        2. uuid of data to write AND data to write, if applicable 
        3. (optional) list of Mac address to filter by
        4. Connection (T/F) Needed to read the sensor 
        """
        #arguments passed in 
        self.config = config 
        self.send_addresses = send_addresses 
        self.receive_addresses = receive_addresses
        self.message_configs = message_configs
        #Necessary methods for the BLE program 
        self.listening_interval = self.config.get("listening_interval", 30)
        self.create_mappings()
        logging.info("Initialized BLE Renogy carrier")
        self.working_mac = None 
        self.working_address = None 
        self.connect_attempts = 0
        self.device_id = 255
        self.poll_interval = self.listening_interval # seconds
        self.adapter = "hci0"
        self.last_message = time.time()
        self.working_mac = None 
        self.working_address = None 
        self.bt1 = None


    def create_mappings(self):
        """
        Takes no arguments
        Uses send and receive addresses to create mappings
        """
        address_info_mapping = {} 
        match_address_mapping = {}
        mac_address_mapping = {}
        address_match_mapping = {}
        address_mac_mapping = {}
        all_addresses = {**self.send_addresses, **self.receive_addresses}
        for address_name, address_config in all_addresses.items():
            address_info = address_config.get("additional_info", {})
            info_dict = {}
            data_uuid = address_info.get("data_uuid", None)
            connection = address_info.get("connection", False)
            write_uuid = address_info.get("write_uuid", None)
            data_to_write = address_info.get("data_to_write", None)
            mac_addresses = address_info.get("mac_addresses", [])
            alias = address_info.get("alias", "")
            info_dict = {
                "data_uuid": data_uuid,
                "connection": connection,
                "write_uuid": write_uuid,
                "data_to_write": data_to_write,
                "mac_addresses": mac_addresses
            }
            address_info_mapping[address_name] = info_dict.copy()
            if data_uuid:
                match_address_mapping[data_uuid] = address_name
                address_match_mapping[address_name] = data_uuid
            for individual_mac in mac_addresses:
                mac_address_mapping[individual_mac] = address_name
            address_mac_mapping[address_name] = mac_addresses
        self.address_info_mapping = address_info_mapping
        self.match_address_mapping = match_address_mapping
        self.mac_address_mapping = mac_address_mapping
        self.address_match_mapping = address_match_mapping
        self.address_mac_mapping = address_mac_mapping
        

    def Bytes2Int(self,bs, offset, length):
            # Reads data from a list of bytes, and converts to an int
            # Bytes2Int(bs, 3, 2)
            ret = 0
            if len(bs) < (offset + length):
                return ret
            if length > 0:
                # offset = 11, length = 2 => 11 - 12
                byteorder='big'
                start = offset
                end = offset + length
            else:
                # offset = 11, length = -2 => 10 - 11
                byteorder='little'
                start = offset + length + 1
                end = offset + 1
            # Easier to read than the bitshifting below
            return int.from_bytes(bs[start:end], byteorder=byteorder)


    def Int2Bytes(self, i, pos = 0):
        # Converts an integer into 2 bytes (16 bits)
        # Returns either the first or second byte as an int
        if pos == 0:
            return int(format(i, '016b')[:8], 2)
        if pos == 1:
            return int(format(i, '016b')[8:], 2)
        return 0


    def create_request_payload(self, device_id, function, regAddr, readWrd):                             
        data = None                                
        if regAddr:
            data = []
            data.append(device_id)
            data.append(function)
            data.append(self.Int2Bytes(regAddr, 0))
            data.append(self.Int2Bytes(regAddr, 1))
            data.append(self.Int2Bytes(readWrd, 0))
            data.append(self.Int2Bytes(readWrd, 1))
            crc = libscrc.modbus(bytes(data))
            data.append(self.Int2Bytes(crc, 1))
            data.append(self.Int2Bytes(crc, 0))
            logging.debug("{} {} => {}".format("create_read_request", regAddr, data))
        return data

    def parse_set_load_response(self, bs):
        FUNCTION = {
            3: "READ",
            6: "WRITE"
        }
        data = {}
        data['function'] = FUNCTION[self.Bytes2Int(bs, 1, 1)]
        data['load_status'] = self.Bytes2Int(bs, 5, 1)
        return data

    def on_connected(self, app):
        #Change here
        logging.debug("Successfully connected")
        self.bt1.poll_params() # OR app.set_load(1)
        #app.set_load(1)

    def on_data_received(self, data):
        try:
            self.bt1.last_time = time.time()
            logging.debug(f"{type(data)}")
            logging.debug(f"Bluetooth message: {data}")
            if data:
                message = {
                            "mac_address": self.working_mac,
                            "packet": data 
                        }
                try:
                    enveloped_message = system_object.system.envelope_message(message, self.working_address)
                    system_object.system.post_messages(enveloped_message, self.working_address)
                except Exception as e:
                    logging.error(f"Could not post BLE Renogy message for reason {e}", exc_info=True)
        except Exception as e:
            logging.error(f"Could not receive BLE Renogy message for reason {e}", exc_info=True)



    def receive(self, address_names, duration):
        """
        Receives a list of addresses and the duration. Depending 
        on the duration and the address, it sets itself
        up to 'receive' messages and post them
        to the system post office along with an address 
        """
        for address_name in address_names:
            try:
                info_dict = self.address_info_mapping.get(address_name, {})
                mac_addresses = info_dict.get("mac_addresses", [])
                alias = info_dict.get("alias", "")
                for mac_addr in mac_addresses:
                    self.bt1 = BTOneApp(self.adapter, mac_addr, self.device_id, self.on_connected, self.on_data_received, self.poll_interval, alias=alias)
                    self.working_mac = mac_addr 
                    self.working_address = address_name 
                self.bt1.sensor_name = address_name
                self.bt1.last_time = time.time()
                needs_connect = True
                while needs_connect == True:
                    needs_connect = False
                    try:
                        self.bt1.connect()
                    except Exception as e:
                        needs_connect = True
                        logging.debug(f"Issue connecting to bluetooth {address_name}")
                        time.sleep(5)                    
            except Exception as e:
                logging.error(f'Could not add init {address_name}.', exc_info=True)
            while True:
                time.sleep(1)

    
    def send(self, address_names, duration, entry_ids=[]):
        """
        Takes in an optional list of entry ids
        Grabs the messages and publishes them, optionally filtering by ID 
        """
        pass 
        #Currently not defined for this bluetooth driver. 


#Licensing:
#This code is generated from: https://github.com/cyrils/renogy-bt 
#It has been modified to fit this use case. 

############################################### Begin BLE.py #######################################

class DeviceManager(gatt.DeviceManager):
    def __init__(self, adapter_name):
        super(). __init__(adapter_name)

        if not self.is_adapter_powered:
            self.is_adapter_powered = True
        logging.debug("Adapter status - Powered: {}".format(self.is_adapter_powered))
        
    def device_discovered(self, device):
        logging.debug("[{}] Discovered, alias = {}".format(device.mac_address, device.alias()))

    def disconnect_devices(self):
        super().remove_all_devices()



class Device(gatt.Device):
    def __init__(self, mac_address, alias, manager, on_resolved, on_data, notify_uuid, write_uuid):
        super(). __init__(mac_address=mac_address, manager=manager)
        self.data_callback = on_data
        self.resolved_callback = on_resolved
        self.manager = manager
        self.notify_char_uuid = notify_uuid
        self.write_char_uuid = write_uuid
        self.device_alias = alias
        self.discovery_timeout = 10

    def connect(self):
        discovering = True; wait = self.discovery_timeout; found = False;

        self.manager.update_devices()
        logging.debug("Starting discovery...")
        self.manager.start_discovery()

        while discovering:
            time.sleep(1)
            logging.debug("Devices found: %s", len(self.manager.devices()))
            for dev in self.manager.devices():
                if dev.mac_address == self.mac_address or dev.alias() == self.device_alias:
                    logging.debug("Found bt1 device %s  [%s]", dev.alias(), dev.mac_address)
                    discovering = False; found = True
            wait = wait -1
            if (wait <= 0):
                discovering = False
        self.manager.stop_discovery()
        if found:
            self.__connect()
        else:
            logging.error("Device not found: [%s], please check the details provided.", self.mac_address)
            self.__gracefully_exit(True)

    def __connect(self):
        try:
            super().connect()
            self.manager.run()
        except Exception as e:
            #MARKED
            logging.error(e)
            self.__gracefully_exit(True)
        except KeyboardInterrupt:
            #MARKED
            self.__gracefully_exit()

    def connect_succeeded(self):
        super().connect_succeeded()
        logging.debug("[%s] Connected" % (self.mac_address))

    def connect_failed(self, error):
        super().connect_failed(error)
        logging.debug("[%s] Connection failed: %s" % (self.mac_address, str(error)))
        #Change here
        self.disconnect()
        time.sleep(5)
        self.services = []
        self.connect()
        raise Exception("Connect failed")

    def disconnect_succeeded(self):
        super().disconnect_succeeded()
        logging.debug("[%s] Disconnected" % (self.mac_address))

    def services_resolved(self):
        super().services_resolved()

        logging.debug("[%s] Resolved services" % (self.mac_address))
        for service in self.services:
            for characteristic in service.characteristics:
                if characteristic.uuid == self.notify_char_uuid:
                    characteristic.enable_notifications()
                    logging.debug("subscribed to notification {}".format(characteristic.uuid))
                if characteristic.uuid == self.write_char_uuid:
                    self.write_characteristic = characteristic
                    logging.debug("found write characteristic {}".format(characteristic.uuid))
        self.resolved_callback()
                    
    def descriptor_read_value_failed(self, descriptor, error):
        logging.debug('descriptor_value_failed')

    def characteristic_enable_notifications_succeeded(self, characteristic):
        logging.debug('characteristic_enable_notifications_succeeded')

    def characteristic_enable_notifications_failed(self, characteristic, error):
        logging.debug('characteristic_enable_notifications_failed')

    def characteristic_value_updated(self, characteristic, value):
        super().characteristic_value_updated(characteristic, value)
        self.data_callback(value)

    def characteristic_write_value(self, value):
        self.write_characteristic.write_value(value)
        self.writing = value

    def characteristic_write_value_succeeded(self, characteristic):
        super().characteristic_write_value_succeeded(characteristic)
        logging.debug('characteristic_write_value_succeeded')
        self.writing = False

    def characteristic_write_value_failed(self, characteristic, error):
        super().characteristic_write_value_failed(characteristic, error)
        logging.debug('characteristic_write_value_failed')
        if error == "In Progress" and self.writing is not False:
            time.sleep(0.1)
            self.characteristic_write_value(self.writing, characteristic)
        else:
            self.writing = False

    def alias(self):
        alias = super().alias()
        if alias:
            return alias.strip()
        return None

    def disconnect(self):
        self.__gracefully_exit()

    def __gracefully_exit(self, connectFailed = False):
        if not connectFailed and super().is_connected():
            logging.debug("Exit: Disconnecting device: %s [%s]", self.alias(), self.mac_address)
            super().disconnect()
        #change
        else:
            super().disconnect()
        self.manager.stop()
        #ANOTHER CHANGE!!!!
        self.services = []
        #A Change here. 
        #os._exit(os.EX_OK)

    #This whole override is a change 
    def properties_changed(self, sender, changed_properties, invalidated_properties):
        logging.debug(f"Sender  {sender}")
        logging.debug(f"Changed properties {changed_properties}")
        logging.debug(f"Invalidated_Properties {invalidated_properties}")
        """
        Called when a device property has changed or got invalidated.
        """
        if 'Connected' in changed_properties:
            if changed_properties['Connected']:
                self.connect_succeeded()
            else:
                pass
                #self.disconnect_succeeded()

        logging.debug(f"self.services {self.services}")

        if ('ServicesResolved' in changed_properties and changed_properties['ServicesResolved'] == 1 and
                not self.services):
            self.services_resolved()

############################################### End BLE.py #########################################


class BTOneApp:
    def __init__(self, adapter_name, mac_address, device_id, on_connected=None, on_data_received=None, interval=30, alias=None):
        self.adapter_name = adapter_name
        self.connected_callback = on_connected
        self.data_received_callback = on_data_received
        self.manager = DeviceManager(adapter_name=self.adapter_name)
        self.notify_char_uuid = "0000fff1-0000-1000-8000-00805f9b34fb"
        self.write_char_uuid = "0000ffd1-0000-1000-8000-00805f9b34fb"
        #REPLACE Notify with data, write with write. 
        self.device = Device(mac_address=mac_address, alias=alias, manager=self.manager, on_resolved=self.__on_resolved, on_data=self.__on_data_received, notify_uuid=self.notify_char_uuid, write_uuid=self.write_char_uuid)
        self.timer = None
        self.timeout = None
        self.interval = interval
        self.data = {}
        #CHANGE
        self.sensor_name = ""
        self.sensor_info = {}
        self.last_time = time.time()
        self.device_id = device_id

    def create_request_payload(self, device_id, function, regAddr, readWrd):                             
        data = None                                
        if regAddr:
            data = []
            data.append(device_id)
            data.append(function)
            data.append(self.Int2Bytes(regAddr, 0))
            data.append(self.Int2Bytes(regAddr, 1))
            data.append(self.Int2Bytes(readWrd, 0))
            data.append(self.Int2Bytes(readWrd, 1))
            crc = libscrc.modbus(bytes(data))
            data.append(self.Int2Bytes(crc, 1))
            data.append(self.Int2Bytes(crc, 0))
            logging.debug("{} {} => {}".format("create_read_request", regAddr, data))
        return data


    def Bytes2Int(self,bs, offset, length):
            # Reads data from a list of bytes, and converts to an int
            ret = 0
            if len(bs) < (offset + length):
                return ret
            if length > 0:
                # offset = 11, length = 2 => 11 - 12
                byteorder='big'
                start = offset
                end = offset + length
            else:
                # offset = 11, length = -2 => 10 - 11
                byteorder='little'
                start = offset + length + 1
                end = offset + 1
            # Easier to read than the bitshifting below
            return int.from_bytes(bs[start:end], byteorder=byteorder)

    def Int2Bytes(self, i, pos = 0):
        # Converts an integer into 2 bytes (16 bits)
        # Returns either the first or second byte as an int
        if pos == 0:
            return int(format(i, '016b')[:8], 2)
        if pos == 1:
            return int(format(i, '016b')[8:], 2)
        return 0


    def connect(self):
        self.device.connect()

    def __on_resolved(self):
        logging.debug("resolved services")
        if self.connected_callback is not None:
            self.connected_callback(self)

    def __on_data_received(self, value):
        operation = self.Bytes2Int(value, 1, 1)
        if operation == 3:
            logging.debug("on_data_received: response for read operation")
            #self.data = parse_charge_controller_info(value)
            if self.data_received_callback is not None:
                #self.data_received_callback(self, self.data)
                self.data_received_callback(value)
        elif operation == 6:
            #self.data = parse_set_load_response(value)
            logging.debug("on_data_received: response for write operation")
            if self.data_received_callback is not None:
                #self.data_received_callback(self, self.data)
                self.data_received_callback(value)
        else:
            logging.warn("on_data_received: unknown operation={}.format(operation)")

    def poll_params(self):
        self.__read_params()
        if self.timer is not None and self.timer.is_alive():
            self.timer.cancel()
        self.timer = Timer(self.interval, self.poll_params)
        curr_time = time.time()
        #Reconnect if it's been 5 min since last message
        #MARKED
        seconds_since = curr_time - self.last_time
        logging.debug(f" {seconds_since} Seconds since last message")
        if curr_time - self.last_time >= 90:
            logging.debug
            logging.info("Attempting to reconnect bluetooth device")
            self.disconnect()
            time.sleep(1)
            self.last_time = time.time()
            self.connect()
        else:
            self.timer.start()


    def __read_params(self):
        READ_PARAMS = {
            'FUNCTION': 3,
            'REGISTER': 256,
            'WORDS': 34
        }
        logging.debug("reading params")
        request = self.create_request_payload(self.device_id, READ_PARAMS["FUNCTION"], READ_PARAMS["REGISTER"], READ_PARAMS["WORDS"])
        self.device.characteristic_write_value(request)

    def set_load(self, value = 0):
        WRITE_PARAMS_LOAD = {
            'FUNCTION': 6,
            'REGISTER': 266
        }
        logging.debug("setting load {}".format(value))
        request = self.create_request_payload(self.device_id, WRITE_PARAMS_LOAD["FUNCTION"], WRITE_PARAMS_LOAD["REGISTER"], value)
        self.device.characteristic_write_value(request)

    def disconnect(self):
        if self.timer is not None and self.timer.is_alive():
            self.timer.cancel()
        self.device.disconnect()
############################################### Begin BTOneApp.py ##################################






def return_object(config={}, send_addresses={}, receive_addresses={}, message_configs={}):
    return BLE_renogy(config=config, send_addresses=send_addresses, receive_addresses=receive_addresses, message_configs=message_configs)


