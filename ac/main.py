import sys
import os
import json
from time import sleep
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from ac.mqtt import mqttPublish
from ac.helper import GetDeviceTopic, TakeImage
from config.mqtt import topicPub
from drive.main import GetACImageInfo

def GetAcImage():
    deviceTopic = GetDeviceTopic()
    mqttPublish(deviceTopic, 'requestServo180:0', False)
    sleep(1)
    TakeImage()
    imageID = GetACImageInfo()
    print("got this image ID: ", imageID)
    response = {"acimageID: ": imageID}
    mqttPublish(topicPub, response, True)