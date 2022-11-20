from PyQt5 import QtWidgets, uic
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtCore import QIODevice

app=QtWidgets.QApplication([])
ui = uic.loadUi("GUI.ui")

from paho.mqtt import client as mqtt_client
import random

broker = '10.0.2.2'
port = 1883
topic = "techno"
client_id = f'python-mqtt-{random.randint(0, 1000)}'

import json

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    #client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def publish(client,topic, msg):
    comand = {
        "cmd":msg
    }
    if msg !="stop":
        comand["val"]=ui.doubleSpinBox.value().__str__()
    comandJS = json.dumps(comand)
    print (comandJS)
    #"""
    result = client.publish(topic, comandJS)
    # result: [0, 1]
    status = result[0]
    if status == 0:
        print(f"Send `{comandJS}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")
    #"""
client = connect_mqtt()
#client=0

def buttonForvard():
    print("buttonForvard")
    publish(client, topic, "forvard")

def buttonBack():
    print("buttonBack")
    publish(client, topic, "back")

ui.pushButton_forward.clicked.connect(buttonForvard)
ui.pushButton_back.clicked.connect(buttonBack)

def buttonLeft():
    print("buttonLeft")
    publish(client, topic, "left")

def buttonRight():
    print("buttonRight")
    publish(client, topic, "right")

ui.pushButton_left.clicked.connect(buttonLeft)
ui.pushButton_right.clicked.connect(buttonRight)

def buttonStop():
    print("buttonStop")
    publish(client, topic, "stop")

ui.stopButton.clicked.connect(buttonStop)

ui.show()
app.exec()
