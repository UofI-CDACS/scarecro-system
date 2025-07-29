import configuration_tester
system_config = {
    "id": "test_device",
    "addresses": [
       "open_meteo_current_in"
    ]
}
configuration_tester.run_test_configuration(system_config)