from paho.mqtt import client as mqtt_client
from config.mqtt import client_id, username, password, broker, port

def connectMqtt():
    client = mqtt_client.Client(client_id + "toSent")
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker as sender")
    else:
        print("Failed to connect, return code %d\n", rc)

