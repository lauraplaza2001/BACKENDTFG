from fastapi import FastAPI, Response    
from fastapi.middleware.cors import CORSMiddleware
import pymongo
import json
from bson import json_util
from bson import ObjectId
from google.oauth2 import id_token
import requests
from google.auth.transport import requests as requestsG
from persistence import Ejercicio



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


#   Permite crear un ejercicio 
@api.post("/ejercicio/crear/",status_code=201)
async def crearEjercicio(ejercicioIn : Ejercicio) :
    ejercicio = {
        "nombre" : ejercicioIn.nombre,
        "descripcion" : ejercicioIn.descripcion,
        "dificultad" : ejercicioIn.dificultad.value,
        "video" : ejercicioIn.video,
        "foto" : ejercicioIn.foto,
        "tips" : ejercicioIn.tips
    }

    db.ejercicio.insert_one(ejercicio)
    return({"mensaje":"Ejercicio creado correctamente"})


#   Devuelve todos los ejercicios de la base de datos 
@api.get("/ejercicio")
async def devolverEjercicios():
    ejercicios = []
    cursor = list(db.ejercicio.find())
    for doc in cursor:
        ejercicios.append(parse_json(doc))
    return ejercicios

#   Permite editar un ejercicio de la base de datos 
@api.put("/ejercicio/editar",status_code=201)
async def editarEjercicio(ejercicioIn: Ejercicio, response: Response) :
    # a la izquierda lo que no se puede cambiar, a la derecha lo que si
    ejercicio = parse_json(db.ejercicio.find_one_and_update({"nombre" : ejercicioIn.nombre}, {"$set" : {"descripcion" : ejercicioIn.descripcion, 
        "dificultad" : ejercicioIn.dificultad.value, "video" : ejercicioIn.video,  "tips" : ejercicioIn.tips}}, upsert=False))

    if ejercicio == None :
        response.status_code = 404  
        return {"message": "Item no encontrado" }
    else:
        print(ejercicio)
        return {"mensaje" : "Vivienda actualizado con éxito"}

