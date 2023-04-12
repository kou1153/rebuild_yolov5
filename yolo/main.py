import sys
import os
import time
import torch
from time import sleep
from pathlib import Path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from config.mqtt import topicPub
from config.drive import currentdayImagePath
from yolo.helper import TakeImage, ResultsParser, GetDeviceTopic
from yolo.mqtt import mqttPublish

model = torch.hub.load('ultralytics/yolov5', 'yolov5n')
model.multi_label = False
model.classes = [0]
model.max_det = 1
model.cpu()

def ImageProcess(uniqueName):
  begin = time.time()
  img = Path(f"{currentdayImagePath}/{uniqueName}.bmp")
  rawResult = model(img)
  print(f"time run ImageProcess is {round(time.time() - begin, 1)} seconds")
  return ResultsParser(rawResult)

def PredictImage():
  breakAllow = True
  commandArr = ["requestServo360:45", "requestServo360:135", "requestServo180:90", "requestServo360:45", "requestServo360:135"]
  deviceTopic = GetDeviceTopic()
  for command in commandArr:
    uniqueName = TakeImage()
    mqttPublish(deviceTopic, command)
    result = ImageProcess(uniqueName)
    if result != "0":
        breakAllow = False
        mqttPublish(topicPub, "1")
        break
    sleep(0.5)
  if breakAllow:
    mqttPublish(topicPub, "0")
  mqttPublish(deviceTopic, "requestResetServo")