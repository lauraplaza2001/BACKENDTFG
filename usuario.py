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

from persistence import Rol
from persistence import Usuario



uri = "mongodb+srv://examen:examen@cluster0.iry9pow.mongodb.net/test"
client_id= "809085480924-kd4b5cqfatoiirqu60ehktf5u7iobnnu.apps.googleusercontent.com"


#   Conexión a la BD
client = pymongo.MongoClient(uri)
db = client.functionaltrainingassistant



api = FastAPI()
origins = ["*"]
api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




    
def parse_json(data):
    return json.loads(json_util.dumps(data))


#   Permite crear un usuario
@api.post("/usuarios/crear/",status_code=201)
async def crearEjercicio(usuarioIn : Usuario) :
    usuario = {
       
        "email" : usuarioIn.email,
        "rol" : Rol.USUARIO.value,
        "token" : usuarioIn.token
      
    }

    db.usuario.insert_one(usuario)
    return({"mensaje":"Usuario creado correctamente"})



@api.get("/usuarios/logIn/{token}")
async def logIn(token: str):
    request = requestsG.Request()

    id_info = id_token.verify_oauth2_token(token, request, client_id, 0)

    nombreUsuario = id_info["given_name"]+" "+id_info["family_name"]
    usuario = parse_json(db.usuario.find_one({"nombre" : nombreUsuario}))
    if usuario == None:
        db.usuario.insert_one({
            "nombre" : nombreUsuario,
            "email" : id_info["email"],
            "rol" : Rol.USUARIO.value
        })

    returnValue = {
        "usuario" : parse_json(db.usuario.find_one({"nombre" : nombreUsuario})),
        "foto" : id_info["picture"]
    }
    return returnValue

#   Devuelve un usuario cuyo id exacto entre por path
@api.get("/usuarios/filter/{id}")                      
async def buscarUsuarioId(id : str):
    usuario = parse_json(db.usuario.find_one({"_id": ObjectId(id)}))
    return usuario
    



#   Devuelve todos los usuarios de la base de datos 
@api.get("/usuarios")
async def devolverUsuarios():
    usuarios = []
    cursor = list(db.usuario.find())
    for doc in cursor:
        usuarios.append(parse_json(doc))
    return usuarios



#   Devuelve un usuario cuyo email exacto entre por path
@api.get("/usuarios/{email}")                      
async def buscarUsuarioEmail(email : str):

    usuario = parse_json(db.usuario.find_one({"email" : email}))
    return usuario



