FROM arm32v6/python:3.8-alpine

RUN apk add gcc musl-dev
RUN pip install Adafruit_Python_DHT influxdb
COPY app.py /app/app.py
ENV DB_HOST=localhost DB_PORT=8086 DB_NAME=weather
ENV SENSOR_GPIO=4 SENSOR_MODEL=22 SENSOR_LOCATION=indoor
ENV SAMPLING_INTERVAL=30 MEASUREMENT_NAME=data
WORKDIR /app
CMD ["python3", "app.py"]
