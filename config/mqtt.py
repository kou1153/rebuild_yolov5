import random

broker = 'rndaedss.ddns.net'
port = 1883
client_id = f'yolo-drive-{random.randint(0, 1000)}'
userid = '640ee59066f4b889269ff405'
username = 'aws'
password = 'Rnd_AEDSS2023'
deviceModule = "cameraDetect"
deviceRoom = "room1"
topicSub = f"{userid}/{deviceModule}/{deviceRoom}/server"
topicPub = f"{userid}/{deviceModule}/{deviceRoom}"
serverRequestCamera = f"serverRequestCamera:{deviceRoom}@{userid}"
serverRequestID = f"serverRequestID:{deviceRoom}@{userid}"
apiURL = f"https://rndaedss.ddns.net/api/v1/yolov5"
apiCameraModule = f"https://rndaedss.ddns.net/api/v1/room/device/{deviceRoom}"
systemKey="4tiNh!B&*$^78PTKqp*v"