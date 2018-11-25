# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt
import time
import json
import threading
import sys

import queue
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
        thread = threading.Thread(target=self.updateTemp, args=())
        thread.daemon = True
        thread.start()
        broker.subscribe(self.id, 0)

    def getTemp(self):
        return self.sensor.get_temperature()

    def writeLog(self):
        return "Success"

    def updateTemp(self):

        self.temp = self.sensor.get_temperature()
        print("friss", self.id, threading.active_count())
        threading.main_thread()
        broker.publish(self.id, self.temp.)
        time.sleep(2)

class RelaySensors:
    def __init__(self,id, config):
        self.id = id
        self.pin = config['pin']


class Controller(object):

    def __init__(self,config):
        self.config = config
        self.tempSensors = [TemperatureSensors(x, y) for (x, y) in config['TemperatureSensors'].items()]
        #self.infraSensors = [RelaySensors(x, y) for (x, y) in config['RelaySensors'].items()]





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

broker = MyMQTTClass()
broker.run()
conf = Controller(json.load(open("set.json",'r',encoding='utf-8')))

while True:

    print('Hajra  hajra')
    # print(time, threading.active_count())
    # data = ["ID","Hofok"]
    # for i in conf.tempSensors:
    #     data.append(i.sysbus,i.temp)
    #     #print(i.sysbus, " : ", i.temp)
    # table = AsciiTable(data)
    # print (table.table)
    time.sleep(1)
