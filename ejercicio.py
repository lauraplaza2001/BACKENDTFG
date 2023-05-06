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
from persistence import Tips
from persistence import Dificultad
from typing import List




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
    tips = []
    gruposMusculares = []

    for tip in ejercicioIn.tips:
        tips.append(tip.value)
   
    for grupoMuscular in ejercicioIn.gruposMusculares:
        gruposMusculares.append(grupoMuscular.value)
    
    ejercicio = {
        "nombre" : ejercicioIn.nombre,
        "descripcion" : ejercicioIn.descripcion,
        "dificultad" : ejercicioIn.dificultad.value,
        "video" : ejercicioIn.video,
        "foto" : ejercicioIn.foto,
        "tips": tips,
        "gruposMusculares": gruposMusculares
    }

    db.ejercicio.insert_one(ejercicio)
    return({"mensaje":"Ejercicio creado correctamente"})




#   Devuelve todos los ejercicios de la base de datos 
@api.get("/ejercicios")
async def devolverEjercicios():
    ejercicios = []
    cursor = list(db.ejercicio.find())
    for doc in cursor:
        ejercicios.append(parse_json(doc))
    return ejercicios


#   Devuelve un ejercicio cuyo id exacto entre por path
@api.get("/ejercicios/filter/{id}")                      
async def buscarEjercicioId(id : str):
    ejercicio = parse_json(db.ejercicio.find_one({"_id": ObjectId(id)}))
    return ejercicio
    





    

#   Permite editar un ejercicio de la base de datos 
@api.put("/ejercicios/editar",status_code=201)
async def editarEjercicio(ejercicioIn: Ejercicio, response: Response) :
    # a la izquierda lo que no se puede cambiar, a la derecha lo que si
    ejercicio = parse_json(db.ejercicio.find_one_and_update({"nombre" : ejercicioIn.nombre}, {"$set" : {"descripcion" : ejercicioIn.descripcion, 
        "dificultad" : ejercicioIn.dificultad.value, "video" : ejercicioIn.video,  "tips" : ejercicioIn.tips}}, upsert=False))

    if ejercicio == None :
        response.status_code = 404  
        return {"message": "Item no encontrado" }
    else:
        print(ejercicio)
        return {"mensaje" : "Ejercicio actualizado con éxito"}

################# CUIDADO CON ESTO ############################ TENGO QUE CAMBIAR LA CONSULTA
#filtrar por nombre de ejercicio


@api.get("/ejercicios/filter/nombre/{nombre}")
async def filtroNombre(nombre: str):
    ejercicios = []
    cursor = db.ejercicio.find()
    for doc in cursor:
        if nombre.casefold() in doc['nombre'].casefold():
            ejercicios.append(parse_json(doc))
    return ejercicios


##filtrar por dificultad 
@api.get("/ejercicios/filter/dificultad/{dificultad}")
async def filtroDificultad(dificultad: str):
    ejercicios = []
   
    ejercicios = parse_json(db.ejercicio.find({"dificultad": dificultad}))
    return ejercicios
    


#filtrar por grupos musculares
@api.get("/ejercicios/filter/gruposMusculares")
async def buscarEjerciciosPorGruposMusculares(grupos_musculares: list):
    # Convertir la lista de grupos musculares a un conjunto
    # para eliminar duplicados y facilitar la búsqueda en MongoDB
    grupos_musculares_set = set(grupos_musculares)

    # Buscar todos los documentos que contengan al menos un grupo muscular de la lista
    ejercicios = db.ejercicio.find({"gruposMusculares": {"$in": list(grupos_musculares_set)}})

    # Convertir el resultado a una lista de diccionarios
    ejercicios_list = [ejercicio for ejercicio in ejercicios]

    return ejercicios_list




