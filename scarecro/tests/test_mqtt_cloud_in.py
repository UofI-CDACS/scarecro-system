
import configuration_tester
system_config = {
    "id": "test_device",
    "addresses": [
        "cloud_mqtt_receive",
        #"printer_send_immediate"
    ]
}
configuration_tester.run_test_configuration(system_config)