import datetime
import subprocess
import httpx
from config.drive import acImagePath, today
from config.mqtt import apiCameraModule, deviceRoom, systemKey, userid

def TakeImage():
  uniqueName = f"{today}_{datetime.datetime.now().strftime('%H%M%S')}"
  subprocess.call(["libcamera-still", "-o", f"{acImagePath}/{uniqueName}.bmp", "--vflip", "-t", "1", "--width", "640", "--height", "480"])
  return uniqueName

def GetDeviceTopic():
  result = httpx.get(apiCameraModule, headers={"system": systemKey, "userid": userid}).json()
  for obj in result:
    if obj["room"] == deviceRoom and obj["deviceModule"] == "CameraPack":
      return obj["topic"]["subscribe"]