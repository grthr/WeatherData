import time
import sys
import datetime
import Adafruit_DHT
import logging as log
from influxdb import InfluxDBClient
import os


log_level = os.environ.get('LOG_LEVEL', 'INFO').upper()
log.getLogger().setLevel(log_level)
log.info('Initializing...')

host = os.environ.get('DB_HOST', 'localhost')
port = int(os.environ.get('DB_PORT', 8086))
dbname = os.environ.get('DB_NAME', 'weather')

sensor_gpio = int(os.environ.get('SENSOR_GPIO', 4))
sensor = int(os.environ.get('SENSOR_MODEL', 22))

measurement = os.environ.get('MEASUREMENT_NAME', 'data')
location = os.environ.get('SENSOR_LOCATION', 'indoor')
interval = int(os.environ.get('SAMPLING_INTERVAL', 30))

client = InfluxDBClient(host=host, port=port, database=dbname)

log.info('Finished initialization.')

try:
    while True:
        humidity, temperature = Adafruit_DHT.read_retry(sensor, sensor_gpio)
        if not humidity or not temperature:
            log.error('Failed to get sensor data.')
            time.sleep(interval)
            continue
        iso = time.asctime(time.gmtime())
        log.debug("[%s] Temp: %s, Humidity: %s" % (iso, temperature, humidity))
        
        data = [
        {
            "measurement": measurement,
            "tags": {
                "location": location,
            },
            "time": iso,
            "fields": {
                "temperature" : temperature,
                "humidity": humidity
            }
        }]
        # Send the JSON data to InfluxDB
        try:
            client.write_points(data)
        except:
            log.error('Failed to write to db.')
            pass
        # Wait until it's time to query again...
        time.sleep(interval)
 
except KeyboardInterrupt:
    pass
