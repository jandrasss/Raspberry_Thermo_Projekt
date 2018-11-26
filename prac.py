# /usr/bin/python3
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
        self.pozicio = config['pozicio']
        # self.precision = 10
        self.sensor = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20, config['sysbus'][3:])
        self.temp = 0
        self.thread = threading.Thread(name=self.id, target=self.updateTemp, args=(), daemon=True)
        # TODO: Ellenőrizni, hogy futnak e a beolvasási szálak.
        broker.subscribe(self.id)

    def checkThread(self):
        if not self.thread.isAlive():
            try:
                self.thread.start()
                print("%s folyamat elindítva" % self.id)
            except:
                print ("Nem sikerült elindítani a beolvasási folyamatot")

    def getTemp(self):
        return self.sensor.get_temperature()

    def writeLog(self):
        return "Success"

    def updateTemp(self):
        while True:
            self.temp = self.sensor.get_temperature()
            # print("friss", self.id, threading.active_count())
            threading.main_thread()
            broker.publish(self.id, self.temp)
            time.sleep(conf.defaultTempUpdateTime)


class RelaySensors:
    def __init__(self,id, config):
        self.id = id
        self.pin = config['pin']


class Controller(object):

    def __init__(self,config):
        self.config = config
        self.defaultTempUpdateTime = config['Config']['defaultTempUpdateTime']
        self.boilerStartDifference = config['Config']['boilerStartDifference']
        self.tempSensors = [TemperatureSensors(x, y) for (x, y) in config['TemperatureSensors'].items()]
        self.boilerUpperIndex = 0
        self.boilerLowerIndex = 0
        self.boilerState = False

        for i in range(0,self.tempSensors.__len__()):
            if self.tempSensors[i].id == "Negyes":
                self.boilerUpperIndex = i
                print("Felső", i)
            if self.tempSensors[i].id == "Otos":
                self.boilerLowerIndex = i
                print("Alsó", i)

        t = threading.Thread(target=self.boilerStart, \
                             args=(int(self.boilerUpperIndex), int(self.boilerLowerIndex), 2,), \
                             daemon=True)
        t.start()

    def boilerStart(self, upperSensor, lowerSensor, difference):
        while True:
            if self.tempSensors[upperSensor].temp-self.tempSensors[lowerSensor].temp>difference and not self.boilerState:
                print("Kazán indul")
                self.boilerState = True
                broker.publish("Kazan", "set.on")
            elif self.tempSensors[upperSensor].temp-self.tempSensors[lowerSensor].temp <= difference and (self.boilerState):
                print("Kazán stop")
                self.boilerState = False
                broker.publish("Kazan", "set.off")

            time.sleep(1)


class MyMQTTClass(mqtt.Client):

    def on_connect(self, mqttc, obj, flags, rc):
        print("rc: "+str(rc))

    def on_message(self, mqttc, obj, msg):
        # print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
        pass

    def on_publish(self, mqttc, obj, mid):
        # print("mid: "+str(mid))
        pass

    def on_subscribe(self, mqttc, obj, mid, granted_qos):
        print("Subscribed: "+str(mid)+" "+str(granted_qos))


    def on_log(self, mqttc, obj, level, string):
        # print(string)
        pass

    def run(self):
        self.connect("10.0.0.12", 1883, 60)
        self.subscribe("pi", 0)
        self.loop_start()

        print("Success")


broker = MyMQTTClass()
broker.run()
conf = Controller(json.load(open("set.json",'r',encoding='utf-8')))

while True:
    for i in conf.tempSensors:
        i.checkThread()
    time.sleep(10)
