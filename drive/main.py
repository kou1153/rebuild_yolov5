import sys
import os
import json
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from config.mqtt import topicPub
from drive.authenticate import creds
from drive.mqtt import mqttPublish
from drive.helper import ValidateUserFolder, ValidateDateFolder, GetAndUploadFile, CleanUp, FetchAllDateFolders, ValidateRoomFolder, FetchAllDateItems, ValidateACFolder, UploadACImage

service = build("drive", "v3", credentials=creds)

def UploadImage():
    try:
        userFolderID = ValidateUserFolder(service)

        roomFolderID = ValidateRoomFolder(service, userFolderID)

        dateFolderID = ValidateDateFolder(service, roomFolderID)

        GetAndUploadFile(service, dateFolderID)

        CleanUp()

    except HttpError as e:
        print(f"Error: {str(e)}")

def GetImageInfo():
    try:
        userFolderID = ValidateUserFolder(service)

        roomFolderID = ValidateRoomFolder(service, userFolderID)

        dateFolderIDs = FetchAllDateFolders(service, roomFolderID)

        listOfImage = FetchAllDateItems(service, dateFolderIDs)

        print("got this list of image: ", listOfImage)
        
        mqttPublish(topicPub, listOfImage)
    
    except HttpError as e:
        print(f"Error: {str(e)}")

def GetACImageInfo():
    try:
        userFolderID = ValidateUserFolder(service)

        acImageFolderID = ValidateACFolder(service, userFolderID)

        imageID = UploadACImage(service, acImageFolderID)

        return imageID

    except HttpError as e:
        print(f"Error: {str(e)}")