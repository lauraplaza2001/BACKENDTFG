import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/drive.file']


def delete_folder(folder_name):
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
        query = "name='{}' and mimeType='application/vnd.google-apps.folder' and trashed=false".format('InfoOpenPose')
        folders = service.files().list(q=query, fields='files(id)').execute().get('files', [])

        if len(folders) == 0:
            print(f'Folder "InfoOpenPose" not found')
            return

        info_folder_id = folders[0].get('id')
        query = "name='{}' and parents='{}' and mimeType='application/vnd.google-apps.folder' and trashed=false".format('json', info_folder_id)
        folders = service.files().list(q=query, fields='files(id)').execute().get('files', [])

        if len(folders) == 0:
            print(f'Folder "json" not found in "InfoOpenPose"')
            return

        json_folder_id = folders[0].get('id')
        query = "name='{}' and parents='{}' and mimeType='application/vnd.google-apps.folder' and trashed=false".format(folder_name, json_folder_id)
        folders = service.files().list(q=query, fields='files(id)').execute().get('files', [])

        if len(folders) == 0:
            print(f'Folder "{folder_name}" not found in "json"')
            return

        folder_id = folders[0].get('id')
        query = "parents='{}' and trashed=false".format(folder_id)
        files = service.files().list(q=query, fields='files(id)').execute().get('files', [])

        for file in files:
            service.files().delete(fileId=file['id']).execute()

        print(f'All files in folder "{folder_name}" have been deleted')
    except HttpError as error:
        print(f'An error occurred: {error}')


def main():
    folder_name = 'perfilJson'  # Enter the name of the folder you want to delete
    delete_folder(folder_name)
    folder_name = 'frontalJson'  # Enter the name of the folder you want to delete
    delete_folder(folder_name)
 

if __name__ == '__main__':
    main()
