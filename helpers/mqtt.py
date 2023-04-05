import time
import json
import httpx
from config.mqtt import deviceRoom, apiURL, topicSub, topicPub, serverRequestCamera, serverRequestID, systemKey, userid
from drive.main import GetImageInfo, UploadImage
from yolo.main import PredictImage

def CaptureDetect(client, topic):
    begin = time.time()
    result = PredictImage()
    print("Predict result: ", result)
    client.publish(topic, result)
    print(f"time run CaptureDetect is {round(time.time() - begin, 1)} seconds")
    UploadImage()

def ImageInfoHandler(client, topic):
    begin = time.time()
    listOfImage = GetImageInfo()
    client.publish(topic, json.dumps(listOfImage))
    print(f"time response ImageInfoHandler is {round(time.time() - begin, 1)} seconds")

def GetSetYolov5():
    result = httpx.get(f"{apiURL}/{deviceRoom}", headers={"system": systemKey, "userid": userid}).json()
    if "success" in result and result["success"] == False:
        result = httpx.post(apiURL, headers={"system": systemKey, "userid": userid}, data={"subscribe": topicSub, "publish": topicPub, "room": deviceRoom, "request": [serverRequestCamera, serverRequestID], "userID": userid})
