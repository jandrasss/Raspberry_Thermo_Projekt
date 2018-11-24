import paho.mqtt.client as mqtt
import time
import json
import threading
import RPi.GPIO as GPIO
import twisted
from w1thermsensor import W1ThermSensor


class TemperatureSensors:
    def __init__(self, id, config):
        self.id = id
        self.sysbus = config['sysbus']
        #self.precision = 10
        self.sensor = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20, config['sysbus'][3:])
        self.temp = 0

        #self.sensor.set_precision(self.precision)
        threading.Thread(target=self.updateTemp()).start()

    def getTemp(self):
        return self.sensor.get_temperature()

    def writeLog(self):
        return "Success"

    def updateTemp(self):
        self.temp = self.sensor.get_temperature()
        time.sleep(5)

class RelaySensors:
    def __init__(self,id, config):
        self.id = id
        self.pin = config['pin']


class Controller(object):

    def __init__(self,config):
        self.config = config
        self.tempSensors = [TemperatureSensors(x, y) for (x, y) in config['TemperatureSensors'].items()]
        #self.infraSensors = [RelaySensors(x, y) for (x, y) in config['RelaySensors'].items()]


conf = Controller(json.load(open("set.json",'r',encoding='utf-8')))
# for i in conf.infraSensors:
#     print(i.id,": ", i.pin)
# for i in conf.tempSensors:
#     print(i.sysbus,": ", i.getTemp())


class MyMQTTClass(mqtt.Client):

    def on_connect(self, mqttc, obj, flags, rc):
        print("rc: "+str(rc))

    def on_message(self, mqttc, obj, msg):
        print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))

    def on_publish(self, mqttc, obj, mid):
        print("mid: "+str(mid))

    def on_subscribe(self, mqttc, obj, mid, granted_qos):
        print("Subscribed: "+str(mid)+" "+str(granted_qos))

    def on_log(self, mqttc, obj, level, string):
        print(string)

    def run(self):
        self.connect("10.0.0.12", 1883, 60)
        self.subscribe("pi", 0)
        self.loop_start()

        print("Success")

MyMQTTClass().run()

# for sensor in W1ThermSensor.get_available_sensors():
#     print("Sensor %s has temperature %.2f" % (sensor.id, sensor.get_temperature()))
while True:

    print('Hajra hajra')
    for i in conf.tempSensors:
        print(i.sysbus, " : ", i.temp)
    time.sleep(1)
