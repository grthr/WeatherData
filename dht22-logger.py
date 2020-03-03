import time
import sys
import datetime
import Adafruit_DHT
from influxdb import InfluxDBClient

# Configure InfluxDB connection variables
host = "192.168.75.134" # red-pi
port = 8086 # default port
dbname = "weather" # the database we created earlier
interval = 30 # Sample period in seconds

# Create the InfluxDB client object
client = InfluxDBClient(host=host, port=port, database=dbname)

# Enter the sensor details
sensor = Adafruit_DHT.DHT22
sensor_gpio = 4

# think of measurement as a SQL table, it's not...but...
measurement = "bluepi-dht22"
# location will be used as a grouping tag later
location = "outdoor"

# Run until you get a ctrl^c
try:
    while True:
        # Read the sensor using the configured driver and gpio
        humidity, temperature = Adafruit_DHT.read_retry(sensor, sensor_gpio)
        iso = time.ctime()
        # Print for debugging, uncomment the below line
        # print("[%s] Temp: %s, Humidity: %s" % (iso, temperature, humidity)) 
        # Create the JSON data structure
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
        client.write_points(data)
        # Wait until it's time to query again...
        time.sleep(interval)
 
except KeyboardInterrupt:
    pass
