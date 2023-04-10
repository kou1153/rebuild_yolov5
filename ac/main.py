import sys
import os
import json
from time import sleep
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from ac.mqtt import connectMqtt
from ac.helper import GetDeviceTopic, TakeImage
from config.mqtt import topicPub
from drive.main import GetACImageInfo

try:
  mqttClient = connectMqtt()
except:
  print("failed to connect mqtt as sender for ac")

def GetAcImage():
    deviceTopic = GetDeviceTopic()
    mqttClient.publish(deviceTopic, "requestServo360:45")
    sleep(1)
    TakeImage()
    imageID = GetACImageInfo()
    response = {"acimageID: ": imageID}
    mqttClient.publish(topicPub, json.dumps(response))