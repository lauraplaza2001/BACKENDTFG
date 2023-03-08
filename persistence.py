from enum import Enum
from typing import Union
from pydantic import BaseModel
from datetime import datetime

class Rol(Enum):
    ADMIN = "ADMIN"
    USUARIO = "USUARIO"

class GruposMusuclares(Enum):
    PIERNAS = "PIERNAS"
    BRAZOS = "BRAZOS"
    ESPALDA = "ESPALDA"
    HOMBROS = "HOMBROS"
    PECHO = "PECHO"
    ABDOMEN = "ABDOMEN"  

class Dificultad(Enum):
    BAJA = 1
    MEDIA = 2
    ALTA = 3

class Tips(Enum):
    ANCHURAPIESCADERA= 1
    ANCHURAPIESHOMBROS= 2
    ANCHURAABIERTOAGARREBARRA= 3
    ANCHURACERRADOAGARREBARRA= 4
    EXTENSIONCOMPLETACADERAYROILLAS= 5
    EXTENSIONCOMPLETACODOS = 6
    BARRAPEGADACUERPO = 7
    RODILLASSIGUENLINEAPIES = 8
    MANTENERESPALDARECTA = 9
    BARRAAPOYADAHOMBROS = 10
    CODOSALTOSPOSICIONFRONTRACK = 11
    BARRASUBEVERTICALMENTE = 12
    ROMPERELPARALELO = 13
    PESODISTRIBUIDOENTODOELPIE = 14

class Usuario(BaseModel):
    id : Union[str,None] = None
    email: str
    rol: Rol
    token: str

class Ejercicio(BaseModel) :
    id : Union[str,None] = None
    nombre : Union[str,None] = None
    descripcion : Union[str,None] = None
    dificultad : Dificultad
    video : Union[str,None] = None
    foto : Union[str,None] = None
    tips : list

class Informe(BaseModel) : 
    id : Union[str,None] = None
    usuario : Union[str,None] = None
    ejercicio : Union[str,None] = None
    resultado : Union[str,None] = None




