import RPi.GPIO as GPIO #may need sudo apt-get -y install python-rpi.gpio
import Adafruit_ADS1x15 #may need sudo apt-get install build-essential python-dev python-smbus python-pip

VOLTAGE_AIR=13560 #voltage reading of sensor in air
VOLTAGE_WATER=5868 #voltage reading of sensor in water
I2C_ADDR = 49
I2C_BUS = 1 #/i2c/dev/1

class ADCMsensor:
  min_moisture = VOLTAGE_AIR
  max_moisture = VOLTAGE_WATER
  adc = Adafruit_ADS1x15.ADS1115(address=I2C_ADDR, bus=I2C_BUS)

  @classmethod
  def get_adc_moisture_reading(cls, channel):
    # get moisture percentage based on raw reading from specified ADC channel
    raw_reading = cls.adc.read_adc(channel, gain=1)
    moisture_percentge = cls.__map(raw_reading)
    return moisture_percentge, raw_reading

  def __map(cls, raw_reading):
    # maps reading to a range specified by the min and max (inspired by map arduino func)
    # formula: (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
    return (raw_reading - cls.min_moisture) * (100-0) / (cls.max_moisture - cls.min_moisture) + 0


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
