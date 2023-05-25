from moisture_sensor import Msensor
from water_pump import WaterPumpRelay
import time


class Controller:
  def __init__(self, msensor, pump, ideal_moisture_level, min_dry_level):
    self.msensor = msensor
    self.pump = pump
    self.is_thirsty = False
    self.ideal_moisture_level = ideal_moisture_level
    self.min_dry_level = min_dry_level

  def __check_moisture__(self):
    moisture_percentage, raw_reading = self.msensor.get_moisture_readings()
    print(f"Moisture level: {moisture_percentage}\nRaw Reading: {raw_reading}")
    return moisture_percentage

  def __pump_water__(self):
    self.pump.release()
    time.sleep(3)
    moisture_percentage = self.__check_moisture__()
    if moisture_percentage >= self.ideal_moisture_level:
      self.is_thirsty = False

  def check_moisture(self):
    moisture_percentage = self.__check_moisture__()
    if moisture_percentage <= self.min_dry_level:
      self.is_thirsty = True

    while self.is_thirsty:
      self.__pump_water__()


def main():
  # Main loop
  time.sleep(3) #initial sleep for pico startup
  sensor1 = Msensor(28)
  pump1 = WaterPumpRelay(22) #Relay in1 set to gpio22
  controller1 = Controller(sensor1, pump1, 90, 22)
  #sensor2 = Msensor(pin)
  #pump2 = WaterPumpRelay(pin)
  #controller2 = Controller(sensor2, pump2, threshold)
  while True:
    controller1.check_moisture()
    #controller2.check_moisture()
    time.sleep(3600)


if __name__ == '__main__':
  main()