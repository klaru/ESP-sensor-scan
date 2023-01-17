from machine import I2C, Pin, freq
from sys import platform

# select GPIO pins
if platform == "esp32":
    pin_scl = 22
    pin_sda = 21
elif platform == "esp8266":
    pin_scl = 5
    pin_sda = 4

import bh1750fvi
import tsl2561
import bme280
from ahtx0 import AHT20
from bme680 import BME680_I2C
from sht30 import SHT30
from sgp30 import SGP30
from sgp40 import SGP40
from scd30 import SCD30
from ssd1305 import SSD1305_I2C
from ssd1306 import SSD1306_I2C
from ds1307 import DS1307

ahtx0_addresses = [0x38]
bmx_addresses = [0x76,0x77]
bh1750_addresses = [0x23,0x5C]
sht3x_addresses = [0x44,0x45]
sgp30_addresses = [0x58]
sgp40_addresses = [0x59]
scd30_addresses = [0x61]
tsl2561_addresses = [0x29,0x39,0x49]
ssd130x_addresses = [0x3C,0x3D]
ds1307_addresses = [0x68]

BME280_REG_CHIPID = 0xD0
BME680_CHIPID = 0x61

i2c = I2C(scl=Pin(pin_scl), sda=Pin(pin_sda))

def bus_scan(i2c,devices):
    for device in devices:
        print()
        for address in ahtx0_addresses:
            if device == address:
                print("AHTx0 temperature, humidity sensor at: ",hex(device))
                try:
                    sensor = AHT20(i2c)
                    print("sensor initialized")
                    print("Temperature = %.0f °C"%sensor.temperature)
                    print("Relative Humidity = %.0f %"%sensor.relative_humidity)
                except OSError:
                    print("sensor doesn't respond")
        for address in bmx_addresses:
            if device == address:
                print("BMx temperature, humidity sensor at: ",hex(device))
                sensor = bme280.Device(address=address, i2c=i2c)
                if sensor.readU8(BME280_REG_CHIPID) == BME680_CHIPID:
                    try:
                        sensor = BME680_I2C(address=address,i2c=i2c)
                        print("sensor initialized")
                        print("Temperature = %0.0f °C" % sensor.temperature)
                        print("Relative Humidity = %0.0f %%" % sensor.relative_humidity)
                        print("Pressure = %0.0f mbar" % sensor.pressure)
                        print("Gas = %d kohm" % (sensor.gas/1000))
                    except OSError:
                        print("sensor doesn't respond")
                else:
                    try:
                        sensor = bme280.BME280(address=address,i2c=i2c)
                        print("sensor initialized")
                        print("Temperature = %.0f °C" % float(sensor.temperature[:-3]))
                        print("Humidity = %.0f %%" % float(sensor.humidity[:-3]))
                        print("Pressure = %.0f hPa" % float(sensor.pressure[:-3]))
                    except OSError:
                        print("sensor doesn't respond")
        for address in bh1750_addresses:
            if device == address:
                print("BH1750 light intensity sensor at: ",hex(device))
                try:
                    sensor = BH1750(i2c,address=address)
                    print("sensor initialized")
                    print("Light intensity = %.0f Lux"%sensor.lux)
                except OSError:
                    print("sensor doesn't respond")
        for address in sht3x_addresses:
            if device == address:
                print("SHT3x temperature, humidity sensor at: ",hex(device))
                try:
                    sensor = SHT31D(i2c)
                    print("sensor initialized")
                    print("Temperature = %.0f °C"%sensor.temperature)
                    print("Relative Humidity = %.0f %"%sensor.relative_humidity)
                except OSError:
                    print("sensor doesn't respond")
        for address in sgp30_addresses:
            if device == address:
                print("SGP30 air quality sensor at: ",hex(device))
                try:
                    sensor = SGP30(i2c)
                    print("sensor initialized")
                    print("CO2 = %d ppm"%sensor.co2_equivalent)
                    print("TVOC = %d ppb"%sensor.total_organic_compound)
                except OSError:
                    print("sensor doesn't respond")
        for address in sgp40_addresses:
            if device == address:
                print("SGP40 air quality sensor at: ",hex(device))
                try:
                    sensor = SGP40(i2c)
                    print("sensor initialized")
                    print("Raw Gas = ", sensor.raw)
                except OSError:
                    print("sensor doesn't respond")
        for address in scd30_addresses:
            if device == address:
                print("SCD30 Temperature, Humidity & CO2 sensor at: ",hex(device))
                try:
                    sensor = SCD30(i2c,address=address)
                    print("sensor initialized")
                    print("Temperature = %.0f °C"%sensor.temperature)
                    print("Relative Humidity = %.0f %"%sensor.relative_humidity)
                    print("CO2 = %d ppm"%sensor.CO2)
                except OSError:
                    print("sensor doesn't respond")
        for address in tsl2561_addresses:
            if device == address:
                print("TSL2561 light intensity sensor at: ",hex(device))
                try:
                    sensor = tsl2561.device(i2c,i2cAddr=address)
                    sensor.init()
                    print("sensor initialized")
                    print("Light intensity = %.0f Lux"%sensor.getLux())
                except OSError:
                    print("sensor doesn't respond")
        for address in ssd130x_addresses:
            if device == address:
                print("SSD130x display at: ",hex(device))
                try:
                    display = SSD1305_I2C(64,48,i2c,addr=address)
                    print("SSD1305 initialized")
                except OSError:
                    try:
                        display = SSD1306_I2C(i2c)
                        print("SSD1306 initialized")
                    except OSError:
                        print("display doesn't respond")
        for address in ds1307_addresses:
            if device == address:
                print("DS1307 RTC at: ",hex(device))
                try:
                    rtc = DS1307(i2c)
                    print("rtc initialized")
                    print("Date/Time = ",rtc.datetime)
                except OSError:
                    print("rtc doesn't respond")

def main():
    print('Scan i2c bus...')
    devices = i2c.scan()
    print('i2c devices found:',len(devices))
    bus_scan(i2c,devices)

if __name__ == "__main__":
     main()



