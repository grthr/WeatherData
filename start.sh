docker run --name weather-data --privileged --restart always -dit -e SENSOR_LOCATION=indoor -e DB_HOST=red-pi weather-data
