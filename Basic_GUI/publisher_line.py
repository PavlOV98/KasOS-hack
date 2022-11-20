from paho.mqtt import client as mqtt_client
import random
import time
import datetime

broker = '10.0.2.2'
port = 1883
topic = "techno"
client_id = f'python-mqtt-{random.randint(0, 1000)}'

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


def publish(client):
    msg_count = 0
    while True:
        time.sleep(5)
        msg = "{\"cmd\": \"auto\", \"markers_screen\": [{\"id\": \"0\", \"x\": \"566\", \"y\": \"422\"}, {\"id\": \"1\", \"x\": \"58\", \"y\": \"60\"}, {\"id\": \"2\", \"x\": \"401\", \"y\": \"33\"}, {\"id\": \"3\", \"x\": \"176\", \"y\": \"231\"}, {\"id\": \"4\", \"x\": \"216\", \"y\": \"210\"}, {\"id\": \"5\", \"x\": \"542\", \"y\": \"220\"}, {\"id\": \"6\", \"x\": \"373\", \"y\": \"265\"}, {\"id\": \"7\", \"x\": \"347\", \"y\": \"267\"}, {\"id\": \"8\", \"x\": \"493\", \"y\": \"218\"}], \"markers_floor\": [{\"id\": \"0\", \"x\": \"566\", \"y\": \"422\"}, {\"id\": \"1\", \"x\": \"58\", \"y\": \"60\"}, {\"id\": \"2\", \"x\": \"401\", \"y\": \"33\"}, {\"id\": \"3\", \"x\": \"176\", \"y\": \"231\"}, {\"id\": \"4\", \"x\": \"216\", \"y\": \"210\"}, {\"id\": \"5\", \"x\": \"542\", \"y\": \"220\"}, {\"id\": \"6\", \"x\": \"373\", \"y\": \"265\"}, {\"id\": \"7\", \"x\": \"347\", \"y\": \"267\"}, {\"id\": \"8\", \"x\": \"493\", \"y\": \"218\"}], \"targets_screen\": [{\"id\": \"0\", \"x\": \"566\", \"y\": \"422\"}, {\"id\": \"1\", \"x\": \"58\", \"y\": \"60\"}, {\"id\": \"2\", \"x\": \"401\", \"y\": \"33\"}, {\"id\": \"3\", \"x\": \"176\", \"y\": \"231\"}, {\"id\": \"4\", \"x\": \"216\", \"y\": \"210\"}, {\"id\": \"5\", \"x\": \"542\", \"y\": \"220\"}, {\"id\": \"6\", \"x\": \"373\", \"y\": \"265\"}, {\"id\": \"7\", \"x\": \"347\", \"y\": \"267\"}, {\"id\": \"8\", \"x\": \"493\", \"y\": \"218\"}], \"robot_screen\": [{\"id\": \"0\", \"x\": \"0\", \"y\": \"0\"}]}"
        result = client.publish(topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"'{datetime.datetime.now().strftime('%H:%M:%S')}' > Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1


def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)


if __name__ == '__main__':
    run()
