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
    ANCHURAABIERTOAGARREBARRA= "ANCHURAABIERTOAGARREBARRA"
    ANCHURACERRADOAGARREBARRA= "ANCHURACERRADOAGARREBARRA"
    EXTENSIONCADERA= "EXTENSIONCADERA"
    EXTENSIONRODILLAS = "EXTENSIONRODILLAS"
    EXTENSIONCOMPLETACODOS = "EXTENSIONCOMPLETACODOS"
    BARRAPEGADACUERPO = "BARRAPEGADACUERPO"
    RODILLASSIGUENLINEAPIES = "RODILLASSIGUENLINEAPIES"
    MANTENERESPALDARECTADESDESUELO = "MANTENERESPALDARECTADESDESUELO"
    MANTENERESPALDARECTADESDENOSUELO = "MANTENERESPALDARECTADESDENOSUELO"
    BARRAAPOYADAHOMBROS = "BARRAAPOYADAHOMBROS"
    CODOSALTOSPOSICIONFRONTRACK = "CODOSALTOSPOSICIONFRONTRACK"
    BARRASUBEVERTICALMENTE = "BARRASUBEVERTICALMENTE"
    ROMPERELPARALELO = "ROMPERELPARALELO"
    PESODISTRIBUIDOENTODOELPIE = "PESODISTRIBUIDOENTODOELPIE"
    SACARCABEZA="SACARCABEZA"

class GruposMusuclares(Enum):
    PIERNAS = "PIERNAS"
    BRAZOS = "BRAZOS"
    ESPALDA = "ESPALDA"
    HOMBROS = "HOMBROS"
    PECHO = "PECHO"
    ABDOMEN = "ABDOMEN"  



class Usuario(BaseModel):
    id : Union[str,None] = None
    email: str
    rol: Rol
    nombre : str
  #  token: str


class Ejercicio2(BaseModel):
    nombre: str
    descripcion: str
    dificultad : Dificultad
    video : str
    foto : str 
    tips : List[Tips]
    gruposMusculares: List[GruposMusuclares]


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
    emailUsuario : Union[str,None] = None
    idEjercicio : Union[str,None] = None
    videoPerfil : Union[str,None] = None
    videoFrontal : Union[str,None] = None



