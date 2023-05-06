from enum import Enum,IntEnum
from typing import Union
from pydantic import BaseModel
from datetime import datetime
from typing import List

class Rol(Enum):
    ADMIN = "ADMIN"
    USUARIO = "USUARIO"



class Dificultad(Enum):
    BAJA = "BAJA"
    MEDIA = "MEDIA"
    ALTA = "ALTA"

class Tips(Enum):
    ANCHURAPIESCADERA= "ANCHURAPIESCADERA"
    ANCHURAPIESHOMBROS= "ANCHURAPIESHOMBROS"
    ANCHURAABIERTOAGARREBARRA= "ANCHURAABIERTOAGARREBARRA"
    ANCHURACERRADOAGARREBARRA= "ANCHURACERRADOAGARREBARRA"
    EXTENSIONCOMPLETACADERAYRODILLAS= "EXTENSIONCOMPLETACADERAYRODILLAS"
    EXTENSIONCOMPLETACODOS = "EXTENSIONCOMPLETACODOS"
    BARRAPEGADACUERPO = "BARRAPEGADACUERPO"
    RODILLASSIGUENLINEAPIES = "RODILLASSIGUENLINEAPIES"
    MANTENERESPALDARECTA = "MANTENERESPALDARECTA"
    BARRAAPOYADAHOMBROS = "BARRAAPOYADAHOMBROS"
    CODOSALTOSPOSICIONFRONTRACK = "CODOSALTOSPOSICIONFRONTRACK"
    BARRASUBEVERTICALMENTE = "BARRASUBEVERTICALMENTE"
    ROMPERELPARALELO = "ROMPERELPARALELO"
    PESODISTRIBUIDOENTODOELPIE = "PESODISTRIBUIDOENTODOELPIE"

class Usuario(BaseModel):
    id : Union[str,None] = None
    email: str
    rol: Rol
    token: str


class GruposMusuclares(Enum):
    PIERNAS = "PIERNAS"
    BRAZOS = "BRAZOS"
    ESPALDA = "ESPALDA"
    HOMBROS = "HOMBROS"
    PECHO = "PECHO"
    ABDOMEN = "ABDOMEN"  

class Ejercicio(BaseModel) :
    id : Union[str,None] = None
    nombre : Union[str,None] = None
    descripcion : Union[str,None] = None
    dificultad : Dificultad
    video : Union[str,None] = None
    foto : Union[str,None] = None
    tips : List[Tips]
    gruposMusculares: List[GruposMusuclares]


class Informe(BaseModel) : 
    id : Union[str,None] = None
    usuario : Union[str,None] = None
    ejercicio : Union[str,None] = None
    resultado : Union[str,None] = None
    videoPerfil : Union[str,None] = None
    videoFrontal : Union[str,None] = None

class InformeAux(BaseModel) :
    idUsuario : Union[str,None] = None
    idEjercicio : Union[str,None] = None
    videoPerfil : Union[str,None] = None
    videoFrontal : Union[str,None] = None



