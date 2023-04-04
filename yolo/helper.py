import datetime
import subprocess
import httpx
from config.drive import currentdayImagePath, today
from config.mqtt import apiCameraModule, deviceRoom, systemKey, userid

def TakeImage():
  uniqueName = f"{today}_{datetime.datetime.now().strftime('%H%M%S')}"
  subprocess.call(["libcamera-still", "-o", f"{currentdayImagePath}/{uniqueName}.bmp", "--vflip", "-t", "1", "--width", "640", "--height", "480"])
  return uniqueName

def ResultsParser(results):
  s = ""
  if results.pred[0].shape[0]:
    for c in results.pred[0][:, -1].unique():
      n = (results.pred[0][:, -1] == c).sum()  # detections per class
      s += f"{n} {results.names[int(c)]}{'s' * (n > 1)}, "  # add to string
  
  if not s.find("person") == -1:
    return s[0]
  else:
    return "0"

def GetDeviceTopic():
  result = httpx.get(apiCameraModule, headers={"system": systemKey, "userid": userid}).json()
  for obj in result:
    if obj["room"] == deviceRoom and obj["deviceModule"] == "CameraPack":
      return obj["topic"]["subscribe"]
