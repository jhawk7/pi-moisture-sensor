import machine
import time

class WaterPumpRelay:
  def __init__(self, pin):
    self.pump_relay = machine.Pin(pin, machine.Pin.OUT)

  def release(self):
    self.pump_relay.on()
    time.sleep(3)
    self.pump_relay.off()

