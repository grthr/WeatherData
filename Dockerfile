FROM python:3.8

COPY dht22-logger.py /app/dht22-logger.py
ADD Adafruit_Python_DHT /app/Adafruit_Python_DHT
ENV DB_HOST=localhost DB_PORT=8086 DB_NAME=weather
ENV SENSOR_GPIO=4 SENSOR_MODEL=22
ENV SAMPLING_INTERVAL=30 MEASUREMENT_NAME=indoor
WORKDIR /app
CMD dht22-logger.py
