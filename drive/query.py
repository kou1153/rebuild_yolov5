from config.drive import today, currentdayImagePath
from config.mqtt import deviceRoom, userid
from googleapiclient.http import MediaFileUpload

def GetRootFolderID(service):
    rootFolderInfo = service.files().list(q=f"name='Image' and mimeType='application/vnd.google-apps.folder'", spaces='drive', fields='files(id, name)').execute()
    return rootFolderInfo["files"][0]["id"]

def GetUserFolderInfo(service, rootFolderID):
    return service.files().list(q=f"name='{userid}' and parents='{rootFolderID}' and mimeType='application/vnd.google-apps.folder'", spaces='drive', fields='files(id, name)').execute()

def GetRoomFolderInfo(service, userFolderID):
    return service.files().list(q=f"name='{deviceRoom}' and parents='{userFolderID}' and mimeType='application/vnd.google-apps.folder'", spaces='drive', fields='files(id, name)').execute()

def GetDateFolderInfo(service, roomFolderID):
    return service.files().list(q=f"name='{today}' and parents='{roomFolderID}' and mimeType='application/vnd.google-apps.folder'", spaces='drive', fields='files(id, name)').execute()

def GetAllDaysInRoom(service, roomFolderID):
    return service.files().list(q=f"parents='{roomFolderID}' and mimeType='application/vnd.google-apps.folder'", spaces='drive', fields='files(id, name)').execute()

def GetAllItemsInDate(service, dateFolderID):
    return service.files().list(q=f"parents='{dateFolderID}'", spaces='drive', fields='files(id, name)').execute()

def CreateFolder(service, file_metadata):
    return service.files().create(body=file_metadata, fields="id").execute()

def SetPermission(service, folderID, request_body):
    return service.permissions().create(fileId = folderID, body = request_body).execute()

def UploadFile(service, file, file_metadata):
    media = MediaFileUpload(f"{currentdayImagePath}/{file}")
    return service.files().create(body=file_metadata, media_body = media, fields="id").execute()