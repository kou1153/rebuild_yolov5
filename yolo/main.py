import sys
import os
import time
import subprocess
from pathlib import Path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

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
  img = Path(f"{currentdayImagePath}/{uniqueName}.bmp")
  rawResult = model(img)
  print(f"time run ImageProcess is {round(time.time() - begin, 1)} seconds")
  return ResultsParser(rawResult)

def PredictImage():
  beginImage = time.time()
  commandArr = ["servo360:45", "servo360:135", "servo180:90", "servo360:45", "servo360:135"]
  deviceTopic = GetDeviceTopic()
  for command in commandArr:
    subprocess.call(["mosquitto_pub", "-h", f"{broker}", "-p", f"{port}", "-t", f"{deviceTopic}", "-m", f"{command}", "-u", f"{username}", "-P", f"{password}"])
    sleep(1)
    TakeImage()
    print("Take a picture now")

  subprocess.call(["mosquitto_pub", "-h", f"{broker}", "-p", f"{port}", "-t", f"{deviceTopic}", "-m", "requestResetServo", "-u", f"{username}", "-P", f"{password}"])
  print(f"time run ImageCapture is {round(time.time() - beginImage, 1)} seconds")

  if not len(os.listdir(currentdayImagePath)) == 0:
    for file in os.listdir(currentdayImagePath):
      result = ImageProcess(file[:file.index(".")])
      if result != "0": 
        return "1"
    return "0"
  else: 
    print("No file to detect")