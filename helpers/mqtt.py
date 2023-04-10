import time
import httpx
from config.mqtt import deviceRoom, apiURL, topicSub, topicPub, serverRequestCamera, serverRequestID, systemKey, userid
from drive.main import GetImageInfo, UploadImage
from yolo.main import PredictImage
from ac.main import GetAcImage

def CaptureDetect():
    begin = time.time()
    PredictImage()
    print(f"time run CaptureDetect is {round(time.time() - begin, 1)} seconds")
    beginUpload = time.time() 
    UploadImage()
    print(f"time run UploadImage is {round(time.time() - beginUpload, 1)} seconds")

def ImageInfoHandler():
    begin = time.time()
    GetImageInfo()
    print(f"time response ImageInfoHandler is {round(time.time() - begin, 1)} seconds")

def AcImageInfoHandler():
    begin = time.time()
    GetAcImage()
    print(f"time response GetAcImage is {round(time.time() - begin, 1)} seconds")

def GetSetYolov5():
    result = httpx.get(f"{apiURL}/{deviceRoom}", headers={"system": systemKey, "userid": userid}).json()
    if "success" in result and result["success"] == False:
        result = httpx.post(apiURL, headers={"system": systemKey, "userid": userid}, data={"subscribe": topicSub, "publish": topicPub, "room": deviceRoom, "request": [serverRequestCamera, serverRequestID], "userID": userid})
