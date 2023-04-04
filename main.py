import asyncio
from paho.mqtt import client as mqtt_client
from config.mqtt import client_id, username, password, broker, port, topicSub, topicPub, serverRequestCamera, serverRequestID, deviceRoom
from helpers.mqtt import CaptureDetect, ImageInfoHandler, GetSetYolov5

def connectMqtt():
    # Set Connecting Client ID
    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        GetSetYolov5()
        print("Connected to MQTT Broker!")
    else:
        print("Failed to connect, return code %d\n", rc)

def subscribe(client: mqtt_client):
    client.subscribe(topicSub)
    client.subscribe(topicPub)
    client.on_message = on_message

def on_message(client, userdata, msg):
    # print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
    asyncio.run(MessageFilter(client, msg.payload.decode()))

async def MessageFilter(client, message):
    if message == serverRequestCamera:
        CaptureDetect(client, topicPub)
        
    if message == serverRequestID:
        ImageInfoHandler(client, topicPub, deviceRoom)

def RunMQTT():
    try:
        client = connectMqtt()
    except:
        print("Failed to connect mqtt")
    else:
        subscribe(client)
        while True:
            client.loop()

if __name__ == "__main__":
  RunMQTT()