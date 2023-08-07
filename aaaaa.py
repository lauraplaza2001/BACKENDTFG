import requests
from fastapi import FastAPI  
from fastapi.middleware.cors import CORSMiddleware
import pymongo
import json
import os
from bson import json_util
from bson import ObjectId
import requests
from persistence import Ejercicio
from persistence import InformeAux
import requests
from reportlab.pdfgen import canvas
import base64
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
import time






    #SEXTO PASO : Analizar los datos dependiendo del movimiento que es (REALMENTE DEPENDE DEL ARRAY DE TIPS)
url = "https://a252-34-87-169-41.ngrok-free.app/openPose"
response = requests.get(url)
if response.status_code == 200:
    # hacer algo con la respuesta
    print("hola")

else:
    print("La solicitud no se pudo completar. Código de estado:", response.status_code)
