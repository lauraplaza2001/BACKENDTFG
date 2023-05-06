from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Define las credenciales
creds = Credentials.from_authorized_user_file('credentials.json', ['https://www.googleapis.com/auth/drive'])

# ID de la carpeta que quieres descargar
folder_id = '1qHWmSp24tOUH7ixf5AKCi3lBC4z8xLdJ'

# Crea la conexión con la API de Drive
service = build('drive', 'v3', credentials=creds)

# Consulta para obtener todos los archivos de la carpeta especificada
query = f"'{folder_id}' in parents"
results = service.files().list(q=query, fields="nextPageToken, files(id, name)").execute()
items = results.get('files', [])

# Descarga los archivos de la carpeta
for item in items:
    file_id = item['id']
    file_name = item['name']
    print(f"Descargando archivo: {file_name} ({file_id})")
    file = service.files().get(fileId=file_id).execute()
    download_url = file.get('webContentLink')
    if download_url:
        response = service.files().get_media(fileId=file_id)
        with open(file_name, 'wb') as f:
            f.write(response.content)
            print(f"Archivo descargado: {file_name}")
    else:
        print(f"No se puede descargar el archivo: {file_name}")
