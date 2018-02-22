#!/usr/bin/python3

import sys
sys.path.append("/home/pi/sds011/Code/")
from sds011 import SDS011
import time
import json


sensor = SDS011("/dev/ttyUSB0")
sensor.reset()
print("Getting workstate...")
print(sensor.workstate)
while True:
    sensor.workstate = SDS011.WorkStates.Measuring
    for t in range(60):
        values = sensor.get_values()
        if values is not None:
            print("PM2.5: ", values[0], ", PM10: ", values[1])
            time.sleep(2)
    
    # open stored data
    with open('/var/www/html/aqi.json') as json_data:
        data = json.load(json_data)
        
    # check if length is more than 100 and delete first element
    if len(data) > 100:
        data.pop(0)
    
    # append new values
    data.append({'pm25': values[0], 'pm10': values[1], 'time': time.strftime("%d.%m.%Y %H:%M:%S")})
    
    # save it
    with open('/var/www/html/aqi.json', 'w') as outfile:
        json.dump(data, outfile)

    print("Going to sleep for 5min...")
    sensor.workstate = SDS011.WorkStates.Sleeping
    print(sensor.workstate)
    time.sleep(300)
