import os
import os.path
import shutil
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from config.drive import rootImagePath, currentdayImagePath, tokenFilePath, credentialFilePath

SCOPES = ["https://www.googleapis.com/auth/drive"]

creds = None

if not len(os.listdir(rootImagePath)) == 0:
    for path in os.listdir(rootImagePath):
        if f"{rootImagePath}/{path}" == currentdayImagePath:
            continue
        shutil.rmtree(f"{rootImagePath}/{path}")

if not os.path.exists(currentdayImagePath):
    os.makedirs(currentdayImagePath)

if os.path.exists(tokenFilePath):
    creds = Credentials.from_authorized_user_file(tokenFilePath, SCOPES)

if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(credentialFilePath, SCOPES)
        creds = flow.run_local_server(port=0)

    with open(tokenFilePath, "w") as token:
        token.write(creds.to_json())
