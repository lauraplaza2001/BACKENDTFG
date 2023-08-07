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
from persistence import GruposMusuclares




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
@api.get("/ejercicios/filter/gruposMusculares/{gruposmusculares}")
async def buscarEjerciciosPorGruposMusculares(gruposmusculares: str):
   # valores_enum = [miembro.value for miembro in GruposMusuclares.__members__.values()]
   # gruposMusculares = []
    #for gm in valores_enum:
     #   if gm in grupos_musculares:
      #      gruposMusculares = grupos_musculares.append(gm)


    ejercicios= []
    gruposMuscularesSplit = gruposmusculares.split(',') if gruposmusculares else []

  

    ejercicios = parse_json(db.ejercicio.find({"gruposMusculares": {"$all": gruposMuscularesSplit}}))
    return ejercicios







   # ejercicios = []
   # ejer= []
    #ejerciciosConGruposMusculares = []
    #cursor = list(db.ejercicio.find())
    #for doc in cursor:
     #   ejer.append(parse_json(doc))

    #for ej in ejer :
     #   for gm in gruposMuscularesSplit:
      #      if gm in cursor.gruposMusculares :
       #         ejerciciosConGruposMusculares.append(ej)


 #   return ejercicios






#   Permite crear un ejercicio 
@api.post("/ejercicios/crear",status_code=201)
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




    
#   Permite editar un ejercicio de la base de datos 
@api.put("/ejercicios/editar",status_code=201)
async def editarEjercicio(ejercicioIn: Ejercicio, response: Response) :
    # a la izquierda lo que no se puede cambiar, a la derecha lo que si
    tips = []
    gruposMusculares = []
    for tip in ejercicioIn.tips:
        tips.append(tip.value)
   
    for grupoMuscular in ejercicioIn.gruposMusculares:
        gruposMusculares.append(grupoMuscular.value)


    ejercicio = parse_json(db.ejercicio.find_one_and_update({"nombre" : ejercicioIn.nombre}, {"$set" :
                                                                                             {"descripcion" : ejercicioIn.descripcion, 
                                                                                             "dificultad" : ejercicioIn.dificultad.value, 
                                                                                             "video" : ejercicioIn.video,  
                                                                                             "tips" : tips,
                                                                                             "gruposMusculares" : gruposMusculares, 
                                                                                             "foto" : ejercicioIn.foto,}}, upsert=False))

    if ejercicio == None :
        response.status_code = 404  
        return {"message": "Item no encontrado" }
    else:
        print(ejercicio)
        return {"mensaje" : "Ejercicio actualizado con éxito"}



#   Devuelve un usuario cuya direccion exacta entre por path
@api.delete("/ejercicios/eliminar/{descripcion}/{nombre}")                      
async def buscarVivienda(nombre : str, descripcion : str , response : Response):
    ejercicio =  parse_json(db.ejercicio.find_one_and_delete({"descripcion" : descripcion, "nombre" : nombre}))

       
    if ejercicio == None :
        response.status_code = 404  
        return {"message": "Item no encontrado" }
    else:
        print(ejercicio)
        return {"mensaje" : "Ejercicio actualizado con éxito"}
 
