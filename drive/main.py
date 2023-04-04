import sys
import os
import time
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from drive.authenticate import creds
from drive.helper import ValidateUserFolder, ValidateDateFolder, GetAndUploadFile, CleanUp, FetchAllDateFolders, ValidateRoomFolder, FetchAllDateItems

service = build("drive", "v3", credentials=creds)

def UploadImage():
    begin = time.time()
    try:
        userFolderID = ValidateUserFolder(service)

        roomFolderID = ValidateRoomFolder(service, userFolderID)

        dateFolderID = ValidateDateFolder(service, roomFolderID)

        GetAndUploadFile(service, dateFolderID)

        CleanUp()

        print(f"time run UploadImage: {round(time.time() - begin, 1)} seconds")

    except HttpError as e:
        print(f"Error: {str(e)}")

def GetImageInfo(deviceRoom):
    begin = time.time()
    try:
        userFolderID = ValidateUserFolder(service)

        roomFolderID = ValidateRoomFolder(service, userFolderID)

        dateFolderIDs, dateFolderNames = FetchAllDateFolders(service, roomFolderID)

        imageDict = FetchAllDateItems(service, dateFolderIDs)

        print(f"time run GetImageInfo: {round(time.time() - begin, 1)} seconds")

        return dateFolderNames, imageDict

    except HttpError as e:
        print(f"Error: {str(e)}")
