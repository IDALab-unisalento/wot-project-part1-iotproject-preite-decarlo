# LIBRERIA PER LETTURA DATI SENSORE DHT TRAMITE ADAFRUIT

import Adafruit_DHT

# Parsing numero sensore con parametro necessario per libreria Adafruit_DHT.
sensor_args = { '11': Adafruit_DHT.DHT11,
                '22': Adafruit_DHT.DHT22,
                '2302': Adafruit_DHT.AM2302 }

def read_temperature_humidity(dht_sensor, pin):
    sensor = sensor_args[str(dht_sensor)]
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

    if humidity is not None and temperature is not None:
        return temperature, humidity
    else:
        print('Failed to get reading. Try again!')
        return None, None
