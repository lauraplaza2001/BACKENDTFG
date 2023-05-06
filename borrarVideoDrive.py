import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/drive.file']



def delete_file(file_name, folder_name):
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
        query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed = false"
        folders = service.files().list(q=query, fields='files(id)').execute().get('files', [])

        if len(folders) == 0:
            print(f'Folder "{folder_name}" not found')
            return

        folder_id = folders[0].get('id')
        query = f"name='{file_name}' and parents in '{folder_id}' and mimeType='video/mp4' and trashed = false"
        files = service.files().list(q=query, fields='files(id)').execute().get('files', [])

        if len(files) == 0:
            print(f'File "{file_name}" not found in folder "{folder_name}"')
            return

        file_id = files[0].get('id')
        service.files().delete(fileId=file_id).execute()
        print(f'File "{file_name}" has been deleted from folder "{folder_name}"')
    except HttpError as error:
        print(f'An error occurred: {error}')




def main():
    folder_name = 'InfoOpenPose'  # Enter the name of the folder where the video file is located
    file_name = 'frontal.mp4'  # Enter the name of the video file you want to delete
    delete_file(file_name, folder_name)
    file_name = 'perfil.mp4'  # Enter the name of the video file you want to delete
    delete_file(file_name, folder_name)
    file_name = 'frontal-openpose.mp4'  # Enter the name of the video file you want to delete
    delete_file(file_name, folder_name)
    file_name = 'perfil-openpose.mp4'  # Enter the name of the video file you want to delete
    delete_file(file_name, folder_name)
 


if __name__ == '__main__':
    main()
