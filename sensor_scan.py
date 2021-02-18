from machine import I2C, Pin, freq

# select GPIO pins
if freq() > 80000000:   # ESP32
    pin_scl = 22
    pin_sda = 21
else:                   # ESP8266
    pin_scl = 5
    pin_sda = 4

pair = [("ahtx0 temperature, humidity sensor", [0x38]),
        ("bmx temperature, humidity sensor ", [0x76,0x77]),
        ("bh1750 light intensity sensor",[0x23]),
        ("sht3x temperature, humidity sensor",[0x44,0x45]),
        ("sgp30 air quality sensor",[0x58]),
        ("sgp40 air quality sensor",[0x59]),
        ("scd30 CO2 sensor",[0x61]),
        ("tsl2561 light intensity sensor",[0x29,0x39,0x49]),
        ("ssd130x display",[0x35,0x36]),
        ("ds1307 RTC",[0x68]),
       ]

i2c = I2C(scl=Pin(pin_scl), sda=Pin(pin_sda))

def main():
    print('Scan i2c bus...')
    devices = i2c.scan()

    print('i2c devices found:',len(devices))
 
    for device in devices:    
        for name, addresses in pair:
            for address in addresses:
                if device == address:
                    print("{} device at : {}".format(name, hex(device)))

                
if __name__ == "__main__":
    main()