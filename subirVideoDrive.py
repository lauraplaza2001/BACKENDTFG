import os
import io
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.http import MediaFileUpload




# Si se modifica algún SCOPE, elimina el archivo token.json
SCOPES = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/drive.file','https://www.googleapis.com/auth/gmail.send']



def upload_video(file_path, folder_id):
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('drive', 'v3', credentials=creds)
        file_name = os.path.basename(file_path)
        file_metadata = {'name': file_name, 'parents': [folder_id]}
        media = MediaFileUpload(file_path, mimetype='video/mp4')
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        print(f'The video "{file_name}" has been uploaded to Google Drive with File ID: {file.get("id")}')
    except HttpError as error:
        print(f'An error occurred: {error}')


def main():
    try:
        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        service = build('drive', 'v3', credentials=creds)
        folder_name = 'InfoOpenPose' 
        query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed = false"
        folders = service.files().list(q=query, fields='files(id)').execute().get('files', [])
        
        if len(folders) == 0:
            folder_metadata = {'name': folder_name, 'mimeType': 'application/vnd.google-apps.folder'}
            folder = service.files().create(body=folder_metadata, fields='id').execute()
            folder_id = folder.get('id')
            print(f'Folder "{folder_name}" has been created with Folder ID: {folder_id}')
        else:
            folder_id = folders[0].get('id')
            print(f'Folder "{folder_name}" already exists with Folder ID: {folder_id}')
        

        file_paths = ['videos/perfil.mp4'] 
        for file_path in file_paths:
            upload_video(file_path, folder_id)


        file_paths2= ['videos/frontal.mp4']
        for file_path in file_paths2:
            upload_video(file_path, folder_id)

    except HttpError as error:
        print(f'An error occurred: {error}')


if __name__ == '__main__':
    main()
