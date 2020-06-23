import time
import sys
import datetime
import Adafruit_DHT
import logging
from influxdb import InfluxDBClient
import os

log.info('Initializing...')

host = os.environ['DB_HOST']
port = int(s.environ['DB_PORT'])
dbname = os.environ['DB_NAME']

sensor_gpio = int(os.environ['SENSOR_GPIO'])
sensor = int(os.environ['SENSOR_MODEL'])

measurement = os.environ['MEASUREMENT_NAME']
interval = int(os.environ['SAMPLING_INTERVAL'])

client = InfluxDBClient(host=host, port=port, database=dbname)
log = logging.getLogger()
log_level = os.environ.get('LOG_LEVEL', 'INFO').upper()

log.info('Finished initialization.')

try:
    while True:
        humidity, temperature = Adafruit_DHT.read_retry(sensor, sensor_gpio)
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
          }
        ]
        # Send the JSON data to InfluxDB
        try:
            client.write_points(data)
        except exc_info:
            log.error('Failed to write to db.', exc_info=exc_info)
            pass
        # Wait until it's time to query again...
        time.sleep(interval)
 
except KeyboardInterrupt:
    pass
