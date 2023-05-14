import json
import paho.mqtt.publish as publish
from config.mqtt import broker, client_id, username, password, broker, port

def mqttPublish(topic, message):
    publish.single(topic, json.dumps(message), hostname=broker, port=1883, auth = {"username": username, "password":password})
