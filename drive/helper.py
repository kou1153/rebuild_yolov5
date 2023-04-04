import os
import os.path
import subprocess
from pathlib import Path

from config.drive import currentdayImagePath, doneUploadList, today
from config.mqtt import deviceRoom, userid
from drive.query import GetRootFolderID, GetUserFolderInfo, GetRoomFolderInfo, GetAllDaysInRoom, GetAllItemsInDate, GetDateFolderInfo, CreateFolder, UploadFile, SetPermission

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
        file_metadata ={
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
    dateFolderIDs, dateFolderNames = list(), list()
    for item in response["files"]:
        dateFolderIDs.append(item["id"])
        dateFolderNames.append(item["name"])
    
    return dateFolderIDs, dateFolderNames

def FetchAllDateItems(service, dateFolderIDs):
    imageList = list()
    for item in dateFolderIDs:
        results = GetAllItemsInDate(service, item)
        imageList += results["files"]
    imageDict, finalDict = dict(), dict()
    for key in imageList:
        name = (key["name"])[:(key["name"]).index("_")]
        id = key["id"]
        if name in imageDict:
            imageDict[name].append(id)
        else:
            imageDict[name] = [id]
    
    finalDict[deviceRoom] = [imageDict]

    return finalDict
