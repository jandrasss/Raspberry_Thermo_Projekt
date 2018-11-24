import paho.mqtt.client as mqtt
import time
import json
import RPi.GPIO as GPIO
import twisted


class TemperatureSensors:
    def __init__(self, id, config):
        self.id = id
        self.sysbus = config['sysbus']
        #self.pin = config['pin']
        self.temp = self.getTemp()
        temp = 0

    def getTemp(self):
        return "temp"


    def writeLog(self):
        return "Success"


class RelaySensors:
    def __init__(self,id, config):
        self.id = id
        self.pin = config['pin']


class Controller(object):

    def __init__(self,config):
        self.config = config
        self.tempSensors = [TemperatureSensors(x, y) for (x, y) in config['TemperatureSensors'].items()]
        #self.infraSensors = [RelaySensors(x, y) for (x, y) in config['RelaySensors'].items()]


# with open('set.json', 'w') as configFile:
#     json.dumps( configFile,  indent=2)



conf = Controller(json.load(open("set.json",'r',encoding='utf-8'))) 
# for i in conf.infraSensors:
#     print(i.id,": ", i.pin)
for i in conf.tempSensors:
    print(i.id,": ", i.id)


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


while True:
    print('Hajra hajra')
    time.sleep(1)
