import os
import time
import torch
from time import sleep
from config.mqtt import broker, port, username, password
from config.drive import currentdayImagePath
from yolo.helper import TakeImage, ResultsParser, GetDeviceTopic

model = torch.hub.load('ultralytics/yolov5', 'yolov5n')
model.multi_label = False
model.classes = [0]
model.max_det = 1
model.cpu()

def ImageProcess(uniqueName):
  begin = time.time()
  img = {currentdayImagePath}/{uniqueName}
  rawResult = model(img)
  print(f"time run ImageProcess is {round(time.time() - begin, 1)} seconds")
  return ResultsParser(rawResult)

def PredictImage():
  commandArr = ["servo360:45", "servo360:135", "servo180:90", "servo360:45", "servo360:135"]
  deviceTopic = GetDeviceTopic()
  for command in commandArr:
    os.system(f"mosquitto_pub -h '{broker}' -p '{port}' -t '{deviceTopic}' -m '{command}' -u '{username}' -P '{password}'")
    sleep(1)
    print("Take a picture now")
    TakeImage()

  os.system(f"mosquitto_pub -h '{broker}' -p '{port}' -t '{deviceTopic}' -m 'requestResetServo' -u '{username}' -P '{password}'")

  begin = time.time()
  if not len(os.listdir(currentdayImagePath)) == 0:
    for file in os.listdir(currentdayImagePath):
      result = ImageProcess(file[:file.index(".")])
      if result != "0": return "1"
    return "0"
  else: 
    print("No file to detect")
  print(f"time run PredictImage is {round(time.time() - begin, 1)} seconds")
