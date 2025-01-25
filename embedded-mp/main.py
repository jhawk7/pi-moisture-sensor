import machine
import network
import config
import json
from mqtt.simple import MQTTClient, MQTTException
from time import sleep

sleep(2)
LED = machine.Pin("LED", machine.Pin.OUT)
VOLTAGE_AIR=49924 #voltage reading of sensor in air
VOLTAGE_WATER=22305 #voltage reading of sensor in water
IDEAL_MOISTURE_LEVEL=90
MOISTURE_THRESHOLD=20
MAX_RETRY=3

class MqttClient:
  def __init__(self):
    client = self.__connectMQTT()
    self.client = client
    self.topic = config.ENV["MQTT_TOPIC"]
    self.isConnected = False
  
  def __connectMQTT(self, counter=1):
    client = MQTTClient(client_id=b"picow_thermo",
      server = config.ENV["MQTT_SERVER"],
      port = 1883,
      user = config.ENV["MQTT_USER"],
      password = config.ENV["MQTT_PASS"],
      keepalive=7000,
      ssl=False
    )
    
    try:
      client.connect()
    except MQTTException:
      LED.value(False)
      sleep(1)
      LED.value(True)
      print("failed to connect to mqtt server")
      counter += 1
      if counter != MAX_RETRY:
        return self.__connectMQTT(counter) #retry
      
      LED.value(False)
      print("max retries for mqtt reached.. backing off")
      return
      
    else:
      self.isConnected = True
      LED.value(False)
      print("connected to mqtt server")
      return client
  
  def publish(self, moisture, raw):
    obj = {"plant-moisture": moisture, "raw-reading": raw, "plant-threshold": MOISTURE_THRESHOLD}
    obj["plant-status"] = "ok" if MOISTURE_THRESHOLD < moisture else "dry"
    obj["action"] = "alert" if obj["plant-status"] == "dry" else "log"
    
    if obj["action"] == "alert":
      obj["alert-msg"] = "Water me! I'm dying!\n\nXOXO, Your house plant"
    
    msg = json.dumps(obj)
    self.client.publish(self.topic, msg) #retain=False, qos=0 by default
    print(f"published values to topic {self.topic}")
  
  def disconnect(self):
    print('disconnecting from mqtt server')
    self.client.disconnect()
    

class Wifi:
  def __init__(self):
    self.wlan = self.__connectWifi()
    
  def __connectWifi(self, counter=1):
    print('Connecting to WiFi Network Name:', config.ENV["SSID"])
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True) # power up the WiFi chip
    print('Waiting for wifi chip to power up...')
    sleep(3) # wait three seconds for the chip to power up and initialize
    wlan.connect(config.ENV["SSID"], config.ENV["WPASS"])
    print('Waiting for access point to log us in.')
    sleep(5)
    
    if wlan.isconnected():
      print('Success! We have connected to your access point!')
      print('Try to ping the device at', wlan.ifconfig()[0])
      LED.value(False)
      return wlan
    elif counter != MAX_RETRY:
      print('Failure! We have not connected to your access point!  Check your config file for errors.')
      LED.value(False)
      counter +=1
      sleep(1)
      LED.value(True)
      print("reconnecting")
      return self.__connectWifi(counter) #retry
    else:
      LED.value(False)
      print('max wifi connect retries reached.. backing off')
      return

  def disconnect(self):
    print('disconnecting from wifi')
    self.wlan.disconnect()
    self.wlan.active(False) #power down wlan chip


def getReading(adc):
  # read moisture sensor
  # formula: (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
  raw = adc.read_u16()
  moisture = (raw - VOLTAGE_AIR) * (100-0) / (VOLTAGE_WATER - VOLTAGE_AIR) + 0
  return raw, moisture


def main():
  adc = machine.ADC(machine.Pin(26))
  while True:
    LED.value(True) # LED will be on until wifi is connected successfully
    wconn = Wifi()
    if wconn.wlan.isconnected:
      sleep(2)
      LED.value(True) # LED will remain on until mqtt is connected successfully
      cMQTT = MqttClient()
      if cMQTT.isConnected:
        raw, moisture = getReading(adc)
        cMQTT.publish(moisture, raw)
        sleep(2)
        print("entering power saver mode..")
        cMQTT.disconnect()
        wconn.disconnect()

    sleep(43200) # check twice daily


if __name__ == "__main__":
  main()

