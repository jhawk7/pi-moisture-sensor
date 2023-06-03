import RPi.GPIO as GPIO
from smbus2 import SMBus
import time

VOLTAGE_AIR=50000 #voltage reading of sensor in air
VOLTAGE_WATER=20500 #voltage reading of sensor in water

class Msensor:
  def __init__(self, pin):
    self.min_moisture = VOLTAGE_AIR
    self.max_moisture = VOLTAGE_WATER
    GPIO.setup(pin, GPIO.IN)
    self.mpin = pin
    self.bus = SMBus(1) #for port 1 (/i2c/dev/1)

  def get_i2c_reading(self):
    #read 16 bytes from addr 0x49 with 0 offset
    block = self.bus.read_i2c_block_data(49, 0, 16)
    
  def get_moisture_readings(self):
    raw_reading = self.mpin.read_u16()
    moisture_percentge = self.__map(raw_reading)
    return moisture_percentge, raw_reading

  def __map(self, raw_reading):
    # maps reading to a range specified by the min and max (inspired by map arduino func)
    # formula: (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
    return (raw_reading - self.min_moisture) * (100-0) / (self.max_moisture - self.min_moisture) + 0


# s = Msensor(28)
# mp, raw = s.get_moisture_readings
# print(f'MP: {mp}\nRAW: {raw}\n\n')


# Left plant dry
# MP: 21.66102
# RAW: 43610

# MP: 21.82373
# RAW: 43562

# MP: 21.44407
# RAW: 43674


# right plant dry
# MP: 24.42712
# RAW: 42794

# MP: 24.21017
# RAW: 42858

# MP: 24.64407
# RAW: 42730


# left plant wet
# MP: 90.28814
# RAW: 23365

# MP: 90.07119
# RAW: 23429


# right plant wet
# MP: 84.42712
# RAW: 25094

# MP: 84.42712
# RAW: 25094
