import os
import base64
import json
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

def guardar_token(token, ruta):
    with open(ruta, 'w') as archivo:
        json.dump(token, archivo)

def cargar_token(ruta):
    with open(ruta, 'r') as archivo:
        return json.load(archivo)

def enviar_correo(destinatario, asunto, mensaje_texto, archivo_adjunto):
    # Credenciales y token de acceso
    token = 'token.json'

    # Configuración de alcance y autorización de OAuth 2.0
    SCOPES= ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/drive.file','https://www.googleapis.com/auth/gmail.send']

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



    # Crear el servicio de la API de Gmail
    service = build('gmail', 'v1', credentials=creds)

    # Crear el mensaje MIME
    mensaje = MIMEMultipart()
    mensaje['to'] = destinatario
    mensaje['subject'] = asunto

    # Adjuntar el mensaje de texto
    mensaje.attach(MIMEText(mensaje_texto, 'plain'))

    # Adjuntar el archivo PDF
    adjunto = MIMEBase('application', 'octet-stream')
    adjunto.set_payload(open(archivo_adjunto, 'rb').read())
    encoders.encode_base64(adjunto)
    adjunto.add_header('Content-Disposition', f'attachment; filename={archivo_adjunto}')
    mensaje.attach(adjunto)

    # Enviar el correo electrónico
    mensaje_raw = base64.urlsafe_b64encode(mensaje.as_bytes()).decode('utf-8')
    service.users().messages().send(userId='me', body={'raw': mensaje_raw}).execute()

    print('Correo electrónico enviado con éxito.')

# Ejemplo de uso
destinatario = 'lauraaplazaa@gmail.com'
asunto = 'Funcional Training Assistance'
mensaje_texto = '¡Ya está disponible tu informe generado por Functional Training Assistance!.'
archivo_adjunto = 'informe.pdf'

enviar_correo(destinatario, asunto, mensaje_texto, archivo_adjunto)
