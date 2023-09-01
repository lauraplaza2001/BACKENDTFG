import os.path
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


SCOPES = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/drive.file']



def download_files(service, folder_id, folder_path):
    page_token = None
    while True:
        response = service.files().list(q=f"'{folder_id}' in parents and trashed = false", fields="nextPageToken, files(id, name, mimeType)", pageToken=page_token).execute()
        files = response.get('files', [])
        page_token = response.get('nextPageToken', None)

        for file in files:
            file_id = file['id']
            file_name = file['name']
            file_path = os.path.join(folder_path, file_name)

            print(f"Downloading {file_path}...")

            if file['mimeType'] == 'application/vnd.google-apps.document':
                file_format = 'application/pdf'
                request = service.files().export_media(fileId=file_id, mimeType=file_format)
                with open(f"{file_path}.pdf", "wb") as f:
                    f.write(request.execute())
            else:
                request = service.files().get_media(fileId=file_id)
                with open(file_path, "wb") as f:
                    f.write(request.execute())

        if page_token is None:
            break



def main():
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
        folder_path = 'InfoOpenPose/json/frontalJson'
        folder_name = 'frontalJson'
        query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed = false"
        folder_id = service.files().list(q=query, fields='files(id)').execute()['files'][0]['id']
        download_files(service, folder_id, folder_path)
    except HttpError as error:
        print(f'An error occurred: {error}')


    try:
        service = build('drive', 'v3', credentials=creds)
        folder_path = 'InfoOpenPose/json/perfilJson'
        folder_name = 'perfilJson'
        query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed = false"
        folder_id = service.files().list(q=query, fields='files(id)').execute()['files'][0]['id']
        download_files(service, folder_id, folder_path)
    except HttpError as error:
        print(f'An error occurred: {error}')



if __name__ == '__main__':
    main()
