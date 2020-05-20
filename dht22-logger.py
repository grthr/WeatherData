import time
import sys
import datetime
import Adafruit_DHT
from influxdb import InfluxDBClient

print "Initializing..."

# Configure InfluxDB connection variables
host = "localhost" # red-pi
port = 8086 # default port
dbname = "weather" # the database we created earlier
interval = 30 # Sample period in seconds

# Create the InfluxDB client object
client = InfluxDBClient(host=host, port=port, database=dbname)

# Enter the sensor details
sensor = Adafruit_DHT.DHT22
sensor_gpio = 4

# think of measurement as a SQL table, it's not...but...
measurement = "redpi-dht22"
# location will be used as a grouping tag later
location = "indoor"

print "Finished initialization."

# Run until you get a ctrl^c
try:
    while True:
        # Read the sensor using the configured driver and gpio
        humidity, temperature = Adafruit_DHT.read_retry(sensor, sensor_gpio)
        iso = time.asctime(time.gmtime())
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
        try:
            client.write_points(data)
        except:
            pass
        # Wait until it's time to query again...
        time.sleep(interval)
 
except KeyboardInterrupt:
    pass
