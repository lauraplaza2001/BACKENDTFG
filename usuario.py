from fastapi import FastAPI, Response    
from fastapi.middleware.cors import CORSMiddleware
import pymongo
import json
from bson import json_util
from bson import ObjectId
from google.oauth2 import id_token
import requests
from google.auth.transport import requests as requestsG
from persistence import Usuario 
from datetime import datetime, timedelta
from time import sleep
import jwt
from enumerados import Rol



uri = "mongodb+srv://examen:examen@cluster0.iry9pow.mongodb.net/test"
client_id= "809085480924-kd4b5cqfatoiirqu60ehktf5u7iobnnu.apps.googleusercontent.com"


#   Conexión a la BD
client = pymongo.MongoClient(uri)
db = client.functionaltrainingassistant



app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)





    
def parse_json(data):
    return json.loads(json_util.dumps(data))



#permite hacer el logIn y crear el usuario si no estaba creado
@app.post("/usuario/logIn/{token}")
async def logIn(token: str):
    request = requestsG.Request()
    id_info = id_token.verify_oauth2_token(token, request, client_id, 0)

    usuario = {
        "email": id_info["email"],
        "rol" : Rol.USUARIO
    }

    db.usuario.insert_one(usuario)
    
    # https://developers.google.com/identity/gsi/web/guides/verify-google-id-token

    returnValue = {
        "usuario": id_info['email'],
        "foto": id_info["picture"]
    }
    
    return returnValue



#   Devuelve todos los usuarios de la base de datos 
@app.get("/usuario")
async def devolverUsuarios():
    usuarios = []
    cursor = list(db.usuarios.find())
    for doc in cursor:
        usuarios.append(parse_json(doc))
    return usuarios




#   Devuelve un usuario cuyo email exacto entre por path
@app.get("/usuarios/{email}")                      
async def buscarUsuario(email : str):

    usuario = parse_json(db.usuario.find_one({"email" : email}))
    return usuario


