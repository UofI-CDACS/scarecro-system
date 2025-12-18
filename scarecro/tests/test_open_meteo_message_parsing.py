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
#Need to come up with several message types and system classes 

forecast_string = '{"latitude":47.685364,"longitude":-116.784294,"generationtime_ms":1.1528730392456055,"utc_offset_seconds":0,"timezone":"GMT","timezone_abbreviation":"GMT","elevation":647.0,"daily_units":{"time":"iso8601","weather_code":"wmo code","temperature_2m_max":"°F","temperature_2m_min":"°F","apparent_temperature_max":"°F","apparent_temperature_min":"°F","sunrise":"iso8601","sunset":"iso8601","sunshine_duration":"s","daylight_duration":"s","uv_index_max":"","uv_index_clear_sky_max":"","rain_sum":"mm","showers_sum":"mm","snowfall_sum":"cm","precipitation_sum":"mm","precipitation_hours":"h","precipitation_probability_max":"%","wind_speed_10m_max":"mp/h","wind_direction_10m_dominant":"°","wind_gusts_10m_max":"mp/h","shortwave_radiation_sum":"MJ/m²","et0_fao_evapotranspiration":"mm","wet_bulb_temperature_2m_mean":"°F","wet_bulb_temperature_2m_max":"°F","wet_bulb_temperature_2m_min":"°F","vapour_pressure_deficit_max":"kPa","surface_pressure_mean":"hPa","surface_pressure_max":"hPa","surface_pressure_min":"hPa","updraft_max":"m/s","visibility_mean":"m","visibility_min":"m","visibility_max":"m","winddirection_10m_dominant":"°","wind_gusts_10m_mean":"mp/h","wind_speed_10m_mean":"mp/h","wind_gusts_10m_min":"mp/h","wind_speed_10m_min":"mp/h","et0_fao_evapotranspiration_sum":"mm","leaf_wetness_probability_mean":"undefined","precipitation_probability_mean":"%","precipitation_probability_min":"%","growing_degree_days_base_0_limit_50":"undefined","relative_humidity_2m_mean":"%","relative_humidity_2m_max":"%","relative_humidity_2m_min":"%","temperature_2m_mean":"°F","apparent_temperature_mean":"°F","cape_mean":"J/kg","cape_max":"J/kg","cape_min":"J/kg","cloud_cover_mean":"%","cloud_cover_max":"%","cloud_cover_min":"%","dew_point_2m_mean":"°F","dew_point_2m_max":"°F","dew_point_2m_min":"°F","snowfall_water_equivalent_sum":"mm","pressure_msl_mean":"hPa","pressure_msl_max":"hPa","pressure_msl_min":"hPa"},"daily":{"time":["2025-07-28","2025-07-29","2025-07-30","2025-07-31","2025-08-01","2025-08-02","2025-08-03"],"weather_code":[0,1,3,51,51,3,3],"temperature_2m_max":[91.1,94.9,99.9,99.5,97.0,90.9,89.6],"temperature_2m_min":[56.1,65.8,62.3,62.1,58.8,58.7,56.1],"apparent_temperature_max":[90.9,93.7,98.1,98.4,94.0,88.0,84.4],"apparent_temperature_min":[52.6,62.5,59.8,60.2,60.4,57.6,52.4],"sunrise":["2025-07-28T12:20","2025-07-29T12:21","2025-07-30T12:22","2025-07-31T12:23","2025-08-01T12:25","2025-08-02T12:26","2025-08-03T12:27"],"sunset":["2025-07-29T03:27","2025-07-30T03:25","2025-07-31T03:24","2025-08-01T03:23","2025-08-02T03:21","2025-08-03T03:20","2025-08-04T03:18"],"sunshine_duration":[50208.10,50192.54,46808.10,49908.24,49831.00,49784.83,50063.18],"daylight_duration":[54458.79,54306.82,54151.75,53993.78,53833.10,53669.89,53504.36],"uv_index_max":[7.25,7.20,7.05,7.00,6.85,6.75,5.95],"uv_index_clear_sky_max":[7.25,7.20,7.25,7.25,7.20,7.00,6.95],"rain_sum":[0.00,0.00,0.00,0.00,0.00,0.00,0.00],"showers_sum":[0.00,0.00,0.00,0.10,1.60,0.00,0.00],"snowfall_sum":[0.00,0.00,0.00,0.00,0.00,0.00,0.00],"precipitation_sum":[0.00,0.00,0.00,0.10,1.60,0.00,0.00],"precipitation_hours":[0.0,0.0,0.0,1.0,10.0,0.0,0.0],"precipitation_probability_max":[1,1,5,18,40,40,12],"wind_speed_10m_max":[7.9,6.7,8.4,5.3,9.6,8.7,9.8],"wind_direction_10m_dominant":[208,336,44,45,221,214,199],"wind_gusts_10m_max":[15.0,9.4,12.5,7.2,18.1,12.8,13.9],"shortwave_radiation_sum":[27.96,28.76,27.10,26.62,24.38,26.29,24.85],"et0_fao_evapotranspiration":[6.35,6.57,7.08,6.12,5.61,6.00,5.86],"wet_bulb_temperature_2m_mean":[57.0,57.6,59.2,62.0,61.7,59.0,54.6],"wet_bulb_temperature_2m_max":[64.1,63.3,66.9,68.6,66.3,64.2,62.6],"wet_bulb_temperature_2m_min":[47.5,51.4,51.1,54.5,57.8,52.6,46.5],"vapour_pressure_deficit_max":[3.98,4.88,5.67,5.61,4.96,4.01,3.85],"surface_pressure_mean":[942.4,945.3,942.5,937.5,940.5,941.0,940.6],"surface_pressure_max":[946.3,948.3,946.1,939.0,943.9,942.9,942.6],"surface_pressure_min":[940.1,943.4,937.6,935.9,934.8,939.1,938.9],"updraft_max":[null,null,null,null,null,null,null],"visibility_mean":[57500.00,72941.66,52755.83,24006.67,23503.33,24140.00,24140.00],"visibility_min":[32000.00,52800.00,24140.00,20940.00,18320.00,24140.00,24140.00],"visibility_max":[78500.00,90000.00,90000.00,24140.00,24140.00,24140.00,24140.00],"winddirection_10m_dominant":[208,336,44,45,221,214,199],"wind_gusts_10m_mean":[6.2,4.3,6.4,4.3,6.7,5.8,6.6],"wind_speed_10m_mean":[3.7,3.1,4.5,3.5,4.4,4.1,4.6],"wind_gusts_10m_min":[1.1,1.1,1.8,2.5,1.6,1.1,2.2],"wind_speed_10m_min":[0.7,0.7,1.1,0.8,1.1,0.9,1.9],"et0_fao_evapotranspiration_sum":[6.35,6.57,7.08,6.12,5.61,6.00,5.86],"leaf_wetness_probability_mean":[null,null,null,null,null,null,null],"precipitation_probability_mean":[0,0,2,12,28,14,4],"precipitation_probability_min":[0,0,0,5,18,7,1],"growing_degree_days_base_0_limit_50":[null,null,null,null,null,null,null],"relative_humidity_2m_mean":[34,24,25,39,57,43,32],"relative_humidity_2m_max":[56,36,57,67,95,70,50],"relative_humidity_2m_min":[20,13,13,13,17,19,16],"temperature_2m_mean":[74.8,80.4,82.3,80.7,74.1,74.6,72.9],"apparent_temperature_mean":[72.3,77.3,79.1,79.8,73.9,72.9,68.8],"cape_mean":[65.4,10.8,128.8,252.9,104.2,55.0,1.7],"cape_max":[390.0,200.0,640.0,920.0,550.0,230.0,30.0],"cape_min":[0.0,0.0,0.0,0.0,0.0,0.0,0.0],"cloud_cover_mean":[1,2,40,73,42,24,56],"cloud_cover_max":[12,42,100,100,100,95,100],"cloud_cover_min":[0,0,0,10,0,0,0],"dew_point_2m_mean":[43.0,38.5,40.6,49.4,53.6,47.9,38.9],"dew_point_2m_max":[50.5,42.8,52.5,54.1,60.0,50.6,43.9],"dew_point_2m_min":[36.4,35.8,31.2,40.0,45.0,42.9,34.3],"snowfall_water_equivalent_sum":[0.00,0.00,0.00,0.00,0.00,0.00,0.00],"pressure_msl_mean":[1014.8,1017.1,1013.8,1008.7,1012.8,1013.3,1013.1],"pressure_msl_max":[1017.9,1019.1,1016.1,1011.4,1017.0,1016.0,1016.3],"pressure_msl_min":[1011.2,1014.7,1006.2,1004.6,1003.7,1009.7,1009.3]}}'
#forecast_string = '{"latitude":47.685364,"longitude":-116.784294,"generationtime_ms":0.15413761138916016,"utc_offset_seconds":0,"timezone":"GMT","timezone_abbreviation":"GMT","elevation":647.0,"current_units":{"time":"iso8601","interval":"seconds","temperature_2m":"°F","relative_humidity_2m":"%","apparent_temperature":"°F","is_day":"","precipitation":"mm","rain":"mm","showers":"mm","snowfall":"cm","weather_code":"wmo code","cloud_cover":"%","pressure_msl":"hPa","surface_pressure":"hPa","wind_speed_10m":"mp/h","wind_direction_10m":"°","wind_gusts_10m":"mp/h"},"current":{"time":"2025-07-29T00:00","interval":900,"temperature_2m":90.5,"relative_humidity_2m":21,"apparent_temperature":87.1,"is_day":1,"precipitation":0.00,"rain":0.00,"showers":0.00,"snowfall":0.00,"weather_code":0,"cloud_cover":0,"pressure_msl":1015.6,"surface_pressure":945.2,"wind_speed_10m":5.2,"wind_direction_10m":162,"wind_gusts_10m":10.3}}'

forecast_msg = json.loads(forecast_string)

enveloped_message = {
            "msg_id": "test_device",
            "msg_time": "now",
            "msg_type": "open_meteo_daily_forecast",
            #"msg_type": "open_meteo_current",
            "msg_content": forecast_msg
            }


system_config = {
    "id": "test_device",
    "addresses": [
        "open_meteo_daily_in"
        #"open_meteo_current_in"
    ],

}

#Init the 
system_object.system = system_class.return_object(system_config=system_config)
system_object.system.init_ecosystem()
system_object.system.start_scheduler()
#Print system update variable 
print("Before open-meteo forecast sent")
time.sleep(2)
system_object.system.post_messages(enveloped_message, "open_meteo_daily_in")
#system_object.system.post_messages(enveloped_message, "open_meteo_current_in")


while True:
    time.sleep(15)
    pass 

