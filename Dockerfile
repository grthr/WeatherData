FROM python:3.8

COPY app.py /app/app.py
ENV DB_HOST=localhost DB_PORT=8086 DB_NAME=weather
ENV SENSOR_GPIO=4 SENSOR_MODEL=22 SENSOR_LOCATION=indoor
ENV SAMPLING_INTERVAL=30 MEASUREMENT_NAME=data
WORKDIR /app
RUN pip install Adafruit_Python_DHT influxdb
CMD ["python3", "app.py"]
