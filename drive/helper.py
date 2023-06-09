import os
import os.path
import subprocess
from pathlib import Path
from copy import deepcopy

from config.drive import currentdayImagePath, doneUploadList, today, acImagePath
from config.mqtt import deviceRoom, userid
from drive.query import GetRootFolderID, GetUserFolderInfo, GetRoomFolderInfo, GetAllDaysInRoom, GetAllItemsInDate, GetDateFolderInfo, CreateFolder, UploadFile, SetPermission, GetAcImageFolderInfo

def ValidateUserFolder(service):
    userFolderInfo = GetUserFolderInfo(service, GetRootFolderID(service))
    if not userFolderInfo['files']:
        file_metadata ={
            "name": f"{userid}",
            "parents": [GetRootFolderID(service)],
            "mimeType": "application/vnd.google-apps.folder"
        }
        response = CreateFolder(service, file_metadata)
        return ConfigPermission(service, response.get("id"))
    else:
        return userFolderInfo["files"][0]["id"]

def ValidateRoomFolder(service, userFolderID):
    roomFolderInfo = GetRoomFolderInfo(service, userFolderID)
    if not roomFolderInfo['files']:
        file_metadata ={
            "name": f"{deviceRoom}",
            "parents": [userFolderID],
            "mimeType": "application/vnd.google-apps.folder"
        }
        response = CreateFolder(service, file_metadata)
        return ConfigPermission(service, response.get("id"))
    else:
        return roomFolderInfo["files"][0]["id"]

def ValidateDateFolder(service, roomFolderID):
    dateFolderInfo = GetDateFolderInfo(service, roomFolderID)
    if not dateFolderInfo['files']:
        file_metadata = {
            "name": f"{today}",
            "parents": [roomFolderID],
            "mimeType": "application/vnd.google-apps.folder"
        }
        response = CreateFolder(service, file_metadata)
        return response.get("id")
    else:
        return dateFolderInfo["files"][0]["id"]

def GetAndUploadFile(service, dateFolderID):
    if not len(os.listdir(currentdayImagePath)) == 0:
        for file in os.listdir(currentdayImagePath):
            file_metadata = {
                "name": file,
                "parents": [dateFolderID]
            }
            response = UploadFile(service, file, file_metadata)
            if "id" in response and len(response) >= 1:
                doneUploadList.append(f"{file}")
        return response.get("id")
    else:
        print("No file in this directory")

def ValidateACFolder(service, userFolderID):
    imageFolderID = GetAcImageFolderInfo(service, userFolderID)
    if not imageFolderID['files']:
        file_metadata = {
            "name": "AC",
            "parents": [userFolderID],
            "mimeType": "application/vnd.google-apps.folder"
        }
        response = CreateFolder(service, file_metadata)
        return response.get("id")
    else:
        return imageFolderID["files"][0]["id"]

def UploadACImage(service, imageFolderID):
    if not len(os.listdir(acImagePath)) == 0:
        for file in os.listdir(acImagePath):
            file_metadata = {
                    "name": file,
                    "parents": [imageFolderID]
                }
            response = service.files().create(body=file_metadata, media_body = f'{Path(f"{acImagePath}/{file}")}', fields="id").execute()
            subprocess.call(["rm", f'{Path(f"{acImagePath}/{file}")}'])
            return response.get("id")
    else:
        print("No file in this directory")

def ConfigPermission(service, folderID):
    request_body = {
        "role": "reader",
        "type": "anyone"
    }
    SetPermission(service, folderID, request_body)
    return folderID

def CleanUp():
    for file in doneUploadList:
        subprocess.call(["rm", f'{Path(f"{currentdayImagePath}/{file}")}'])
    doneUploadList.clear()

def FetchAllDateFolders(service, roomFolderID):
    response = GetAllDaysInRoom(service, roomFolderID)
    dateFolderIDs =  list()
    for item in response["files"]:
        dateFolderIDs.append(item["id"])
    
    return dateFolderIDs

def FetchAllDateItems(service, dateFolderIDs):
    imageList = list()
    for item in dateFolderIDs:
        results = GetAllItemsInDate(service, item)
        imageList += results["files"]
    
    listOfImage = list()

    imageDict = {"date": "", "ids": []}

    previous = ""

    for key in imageList:
        date = (key["name"])[:(key["name"]).index("_")]
        id = key["id"]
        
        if previous == "" and imageDict["date"] == "":
            imageDict["date"] = date
            previous = date

        if previous == date:
            imageDict["ids"].append(id)
            previous = date

        if previous != date and previous != "":
            listOfImage.append(deepcopy(imageDict))
            imageDict["ids"].clear()
            imageDict["date"] = date
            imageDict["ids"].append(id)
            previous = date

        if key == imageList[-1]:
            listOfImage.append(deepcopy(imageDict))

    return listOfImage
