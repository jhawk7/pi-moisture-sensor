import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

class WaterPumpRelay:
  def __init__(self, pin):
    GPIO.setup(pin, GPIO.OUT)
    self.pump_relay = pin

  def release(self):
    GPIO.output(self.pump_relay, GPIO.HIGH)
    time.sleep(3)
    GPIO.output(self.pump_relay, GPIO.LOW)
