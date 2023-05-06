from fastapi import FastAPI, Response    
from fastapi.middleware.cors import CORSMiddleware
import pymongo
import json
import os
from bson import json_util
from bson import ObjectId
from google.oauth2 import id_token
import requests
from google.auth.transport import requests as requestsG
from persistence import Ejercicio
from persistence import Tips
from persistence import Informe
from persistence import InformeAux
import requests



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



#   Devuelve todos los informes de la base de datos 
@api.get("/informes")
async def devolverInformes():
    informes = []
    cursor = list(db.informe.find())
    for doc in cursor:
        informes.append(parse_json(doc))
    return informes


 


#   Permite crear un informe
@api.post("/informes/crear/",status_code=201)
async def crearEjercicio(informeIn : InformeAux) :
    informeAux = {
        "idUsuario" : informeIn.idUsuario,
        "idEjercicio" : informeIn.idEjercicio,
        "videoFrontal" : informeIn.videoFrontal,
        "videoPerfil" : informeIn.videoPerfil,
    }

    ###################################
    # busco el ejercicio dado el id primero y modifico los parametros de abajo
    resultado = generarResultados(informeIn.idEjercicio, informeIn.videoFrontal, informeIn.videoPerfil)
    informe = {

        "videoFrontal" : informeIn.videoFrontal,
        "videoPerfil" : informeIn.videoPerfil,
        "resultado" : resultado



    }

    db.informe.insert_one(informe)
    return({"mensaje":"Informe creado correctamente"})




def extract_pose_keypoints_2d(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data['people'][0]['pose_keypoints_2d']




def generarResultados(ejercicio : Ejercicio, videoFrontal : str, videoPerfil: str) :

    #PRIMER PASO : me descargo los videos de cloudinary y les cambio el nombre para ello tengo que hacer un get
    responseFrontal = requests.get(videoFrontal)
    with open('videos/frontal.mp4', 'wb') as f:
        f.write(responseFrontal.content)

    responsePerfil = requests.get(videoPerfil)
    with open('videos/perfil.mp4', 'wb') as f:
        f.write(responsePerfil.content)


    #SEGUNDO PASO : los subo a google drive con el nombre perfil.mp4 y frontal.mp4



    #SEGUNDO PASO:  accedo a Flask con el /openPose (el resto del enlace es dinamico). Cuando se termine el get, ya tenemos los keypoint guardados en google drive
    #no se si espera a hacer el get y luego ya continua
    url = "https://888e-34-143-239-250.ngrok-free.app/openPose"
    response = requests.get(url)

    if response.status_code == 200:
        # hacer algo con la respuesta
        print(response.text)
    else:
        print("La solicitud no se pudo completar. Código de estado:", response.status_code)

    
    #TERCER PASO : descargar de Google Drive los keyPoints
    os.system('python descargarGoogleDrive.py')

    #CUARTO PASO : Analizar los datos dependiendo del movimiento que es (REALMENTE DEPENDE DEL ARRAY DE TIPS)
    url= "https://localhost:8001/ejercicios/filter/"+ idEjercicio
    response = requests.get(url)
    if response.status_code == 200:
        # hacer algo con la respuesta
        ejercicio = response.json() # es un objeto
        print(ejercicio)
    else:
        print("La solicitud no se pudo completar. Código de estado:", response.status_code)


    # con esto tenemos el numero de archivos, para ver sobre cuantos keypoints comprobamos
    #tambien tenemos los archivos en forma de array
    dir_path = 'InfoOpenPose/json/frontalJson'
    filesFrontal = os.listdir(dir_path)
    keypointsFrontal= len(filesFrontal)
    dir_path = 'InfoOpenPose/json/perfilJson'
    filesPerfil = os.listdir(dir_path)
    keypointsPerfil= len(filesPerfil)
    correcto = []
    incorrecto= []



##esta mal es anchura de pies , no de rodilla
    for tip in ejercicio.tips :

        if tip == "ANCHURAPIESCADERA" :    #frontal
            contador= 0 
            secumple= 0
            while contador < 7 :
                archivo_json= 'InfoOpenPose/json/frontalJson/' + keypointsFrontal[contador]
                perfil_pose_keypoints_2d = extract_pose_keypoints_2d(archivo_json)

                caderaDer_x=perfil_pose_keypoints_2d[9*3]
                caderaIzq_x=perfil_pose_keypoints_2d[12*3]
                tobilloDer_x=perfil_pose_keypoints_2d[11*3]
                tobilloIzq_x=perfil_pose_keypoints_2d[14*3]


                if (abs(tobilloIzq_x - caderaIzq_x)) > 40 and abs(tobilloDer_x -caderaDer_x) > 40 :
                    secumple = secumple +1 
                
                contador = contador +1
            
            if secumple > (0.7* contador):
             correcto.append("Anchura de los pies es igual a la cadera")
            else : 
                incorrecto.append("La anchura de los pies debe estara la altura de la cadera")



        if tip == "ANCHURAPIESHOMBROS":
            contador= 0 
            secumple= 0
            while contador < 7 :
                archivo_json= 'InfoOpenPose/json/frontalJson/' + keypointsFrontal[contador]
                perfil_pose_keypoints_2d = extract_pose_keypoints_2d(archivo_json)


                tobilloDer_x=perfil_pose_keypoints_2d[11*3]
                tobilloIzq_x=perfil_pose_keypoints_2d[14*3]
                hombroIzq_x=perfil_pose_keypoints_2d[5*3]
                hombroDer_x =perfil_pose_keypoints_2d[2*3]


                if (abs(tobilloIzq_x - hombroIzq_x)) > 1 and abs(tobilloDer_x -hombroDer_x) > 1 :
                    secumple = secumple +1 
                
                contador = contador +1
            
            if secumple > (0.7* contador):
             correcto.append("Anchura de los pies es igual a los hombros")
            else : 
                incorrecto.append("La anchura de los pies debe estar a la altura de los hombros")




        if tip == "ANCHURAABIERTOAGARREBARRA" : # frontal
    
            contador=0
            secumple=0
            cierraAgarre=0
            abreAgarre=0
            cotaInferior = 50
            cotaSuperior = 60


            while(contador < 7) :
                archivo_json= 'InfoOpenPose/json/frontalJson/' + keypointsFrontal[contador]
                perfil_pose_keypoints_2d = extract_pose_keypoints_2d(archivo_json)
                muñecaDer_x=perfil_pose_keypoints_2d[4*3]
                muñecaIzq_x=perfil_pose_keypoints_2d[7*3]
                rodillaDer_x=perfil_pose_keypoints_2d[10*3]
                rodillaIzq_x=perfil_pose_keypoints_2d[13*3]

                if((rodillaDer_x - muñecaDer_x) > cotaSuperior and (muñecaIzq_x-rodillaIzq_x > cotaSuperior)) :
                    cierraAgarre= cierraAgarre+1
                elif( (rodillaDer_x-muñecaDer_x)<cotaInferior and (muñecaIzq_x-rodillaIzq_x) < cotaInferior ):
                    abreAgarre = abreAgarre +1
                else: 
                    secumple = secumple+1

                contador=contador + 1
            
            if(secumple >= 0.6 * contador) :
                correcto.append("Agarre abierto")
            elif(cierraAgarre > 0.6 * contador):
                incorrecto.append("Agarre demasiado abierto, junte más las manos")
            elif(abreAgarre > 0.6 *contador):
                incorrecto.append("Agarre demasiado cerrado, separe más las manos")     
            else: correcto.append("Error, no se como es el agarre")
 
 


        elif tip == "ANCHURACERRADOAGARREBARRA": 
            contador=0
            secumple=0
            cierraAgarre=0
            abreAgarre=0
            cotaInferior = 50
            cotaSuperior = 60


            while(contador < 7) :
                archivo_json= 'InfoOpenPose/json/frontalJson/' + keypointsFrontal[contador]
                perfil_pose_keypoints_2d = extract_pose_keypoints_2d(archivo_json)
                muñecaDer_x=perfil_pose_keypoints_2d[4*3]
                muñecaIzq_x=perfil_pose_keypoints_2d[7*3]
                rodillaDer_x=perfil_pose_keypoints_2d[10*3]
                rodillaIzq_x=perfil_pose_keypoints_2d[13*3]

                if((rodillaDer_x-muñecaDer_x) > cotaSuperior and (muñecaIzq_x-rodillaIzq_x > cotaSuperior)) :
                    cierraAgarre= cierraAgarre+1
                elif( (rodillaDer_x-muñecaDer_x)<cotaInferior and (muñecaIzq_x-rodillaIzq_x) < cotaInferior ):
                    abreAgarre = abreAgarre +1
                else: 
                    secumple = secumple+1

                contador=contador + 1
            
            if(secumple >= 0.6 * contador) :
                correcto.append("Agarre cerrado ")
            elif(cierraAgarre > 0.6 * contador):
                incorrecto.append("Agarre demasiado abierto, junte más las manos")
            elif(abreAgarre > 0.6 *contador):
                incorrecto.append("Agarre demasiado cerrado, separe más las manos")     
            else: correcto.append("Error, no se como es el agarre")
 


        elif tip == "BARRAPEGADACUERPO": #muñeca-talon(perfil, solo me intereesa el lado izquierdo)
            contador=0
            nopegada=0
            cota=4

            for keypoint in keypointsPerfil :
                archivo_json= 'InfoOpenPose/json/perfilJson/' + keypoint
                perfil_pose_keypoints_2d = extract_pose_keypoints_2d(archivo_json)

                muñecaIzq_x=perfil_pose_keypoints_2d[7*3]
                talonIzq_x=perfil_pose_keypoints_2d[21*3]

                if( abs(muñecaIzq_x-talonIzq_x) >  cota):
                    nopegada = nopegada+1

            if nopegada > 3:
                incorrecto.append("Manten la barra pegada a tu cuerpo durante todo el movimiento")
            else:
                correcto.append("Barra pegada al cuerpo")      




        elif tip == "EXTENSIONCADERA": #
            caderafinal=0
            nelementos = len(keypointsFrontal)
            contador= 0.8*nelementos
            cotaExtensionCadera=10
            cota =2 # numero de  vecesque debe cumplirse la extension de cadera 

     

            while (contador < nelementos) :
                archivo_json= 'InfoOpenPose/json/frontalJson/' + keypointsFrontal[contador]
                perfil_pose_keypoints_2d = extract_pose_keypoints_2d(archivo_json)

                hombroIzq_x=perfil_pose_keypoints_2d[5*3]
                caderaIzq_x=perfil_pose_keypoints_2d[12*3]

                extCadera = abs(caderaIzq_x-hombroIzq_x)
    
                if( extCadera <= cotaExtensionCadera) :
                    caderafinal = caderafinal+1


            if(caderafinal >=cota )  :
                correcto.append("Exntesión de cadera final") 
            else:
                incorrecto.append("Debe extender la cadera al final del movimiento")



        elif tip == "EXTENSIONRODILLAS":#PRACTICAMENTE MISMO CODIGO QEU ARRIBA
            rodillafinal=0
            nelementos = len(keypointsFrontal)
            contador= 0.8*nelementos
            cotaExtensionRodilla=10
            cota =2 # numero de  vecesque debe cumplirse la extension de cadera 


            while (contador < nelementos) :
                archivo_json= 'InfoOpenPose/json/frontalJson/' + keypointsFrontal[contador]
                perfil_pose_keypoints_2d = extract_pose_keypoints_2d(archivo_json)

                rodillaIzq_x=perfil_pose_keypoints_2d[13*3]
                talonIzq_x=perfil_pose_keypoints_2d[21*3]



                extRodilla = abs(rodillaIzq_x-talonIzq_x)
                
              
    
                if( extRodilla <= cotaExtensionRodilla) :
                    rodillafinal = rodillafinal+1


            if(rodillafinal >=cota )  :
                correcto.append("Extensión de rodilla final") 
            else:
                incorrecto.append("Debe extender la rodilla al final del movimiento")




        elif tip == "PESODISTRIBUIDOENTODOELPIE": #talon-bigtoe eje y (perfil)
            pesoPuntillas=0
            pesoTalones=0
            cota = 2 # +- para que no se considere que se cumple
            limiteVeces=3 # cuantas veces debe ocurrir para

            for keypoint in keypointsPerfil :
                archivo_json= 'InfoOpenPose/json/perfilJson/' + keypoint
                perfil_pose_keypoints_2d = extract_pose_keypoints_2d(archivo_json)

                talonIzq_y=perfil_pose_keypoints_2d[21*3+1]
                bigToeIzq_y=perfil_pose_keypoints_2d[19*3+1]

                diferencia= bigToeIzq_y-talonIzq_y

                if(diferencia > cota) :
                    pesoPuntillas= pesoPuntillas+1 
                elif(diferencia < (-cota)) :
                    pesoTalones+1
                  
                
                
            if (pesoPuntillas > limiteVeces) :
                incorrecto.append("Apoye el talón durante todo el movimiento")
            elif (pesoTalones > limiteVeces):
                incorrecto.append("Apoye la punta de los pies durante todo el movimiento")
            else:
                correcto.append("Peso bien distribuido en los pies")




        elif tip == "BARRASUBEVERTICALMENTE": #codo-muñeca, perfil
             # y recuerda que los hombros deben quedar por detras de la oreja
            margen=0.5 # margen de error
            limiteVeces= 3
            contador = 0 

            for keypoint in keypointsPerfil :
                archivo_json= 'InfoOpenPose/json/perfilJson/' + keypoint
                perfil_pose_keypoints_2d = extract_pose_keypoints_2d(archivo_json)
               
                muñecaIzq_x=perfil_pose_keypoints_2d[7*3]
                codoIzq_x=perfil_pose_keypoints_2d[6*3]

                #muñeca - codos es positivo si está bien
                diferencia= muñecaIzq_x-codoIzq_x
                if(diferencia + margen  < 0) # si la diferencia + la cota me sale negativo es porque la muñeca está adelantando al codo
                    contador = contador+1







  #       elif tip== "EXTENSIONCOMPLETACODOS":


 #        


   #      elif tip == "RODILLASSIGUENLINEAPIES":

  #       elif tip == "MANTENERESPALDARECTA":

    #     

      #   elif tip == "CODOSALTOSPOSICIONFRONTRACK":
        


   #      elif tip == "ROMPERELPARALELO":
        
   #      elif tip == "PESODISTRIBUIDOENTODOELPIE":
            
            





# y alfinal del todo borramos los recursos de drive
    os.system('python borrarVideoDrive.py')
    os.system('python borrarCarpetaDrive.py')
   

# y borramos los recursos de mi proyecto
    os.system('python borrarInfoCarpetasProyecto.py')

   



    return "hola"



