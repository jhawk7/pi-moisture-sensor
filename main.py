from pkg.moisture_sensor import ADCMsensor
from pkg.water_pump import WaterPumpRelay
from pkg.opentel import Opentel
import time


class Controller:
  def __init__(self, adc_channel, pump, meter, ideal_moisture_level, min_dry_level):
    self.pump = pump
    self.adc_channel = adc_channel
    self.is_thirsty = False
    self.ideal_moisture_level = ideal_moisture_level
    self.min_dry_level = min_dry_level
    self.latest_moisture_reading = None
    #will this run async?
    meter.create_observable_guage(
      name="{meter.name}.moisture_percentage", 
      description="plant moisture percentage",
      callback=self.poll_moisture_reading,
      unit="percentage(%)",
      value_type=float
    )

  def __check_moisture(self):
    moisture_percentage, _ = ADCMsensor.get_adc_moisture_reading(self.adc_channel)
    #print(f"Moisture level: {moisture_percentage}\nRaw Reading: {raw_reading}")
    self.latest_moisture_reading = moisture_percentage
    return moisture_percentage

  def __pump_water(self):
    self.pump.release()
    time.sleep(3)
    #moisture_percentage = self.__check_moisture()
    if self.latest_moisture_reading >= self.ideal_moisture_level:
      self.is_thirsty = False

  def check_moisture(self):
    #moisture_percentage = self.__check_moisture()
    if self.latest_moisture_reading <= self.min_dry_level:
      self.is_thirsty = True

    while self.is_thirsty:
      self.__pump_water()

  def poll_moisture_reading(self, result):
    #observable opentel counter
    moisture_percentage = self.__check_moisture()
    result.Observe(moisture_percentage, ("read.type", "moisture_percentage"))
    result.Observe(self.ideal_moisture_level, ("read.type", "ideal_moisture_level"))
    result.Observe(self.min_dry_level, ("read.type", "min_dry_level"))


def main():
  # Main loop
  #sensor1, sensor2 = Msensor(23), Msensor(14)
  pump1, pump2 = WaterPumpRelay(24), WaterPumpRelay(15) #Relay in1 set to gpio22
  opentel = Opentel()
  meter1, meter2 = opentel.get_meter("plant1"), opentel.get_meter("plant2")
  controller1 = Controller(0, pump1, meter1, 90, 22)
  controller2 = Controller(1, pump2, meter2, 90, 22)
  
  while True:
    controller1.check_moisture()
    controller2.check_moisture()
    time.sleep(3600)


if __name__ == '__main__':
  main()
  