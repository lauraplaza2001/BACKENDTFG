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
import config




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
@api.post("/informes/crear",status_code=201)
async def crearInforme(informeIn : InformeAux) :

    informeAux = {
            "idUsuario" : informeIn.idUsuario,
            "emailUsuario" : informeIn.emailUsuario,
            "idEjercicio" : informeIn.idEjercicio,
            "videoFrontal" : informeIn.videoFrontal,
            "videoPerfil" : informeIn.videoPerfil
        }

    resultado = generarResultados(informeAux["idEjercicio"], informeAux["videoFrontal"], informeAux["videoPerfil"],informeAux["emailUsuario"])
    informe = {
            "videoFrontal" : informeAux['videoFrontal'],
            "videoPerfil" : informeAux['videoPerfil'],
            "resultado" : resultado,
            "usuario" : informeAux['idUsuario'],
            "ejercicio" : informeAux['idEjercicio']



        }
    db.informe.insert_one(informe)
    print('Informe creado')

    return({"mensaje":"Informe creado correctamente"})




def parse_json(data):
    return json.loads(json_util.dumps(data))



def extract_pose_keypoints_2d(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data['people'][0]['pose_keypoints_2d']








def generarResultados(idEjercicio : str, videoFrontal : str, videoPerfil: str, emailUsuario : str) :
    informe = ""
    #Nos aseguramos que los recursos están limpios:
    os.system('python borrarVideoDrive.py')
    os.system('python borrarCarpetaDrive.py')
    os.system('python borrarInfoCarpetasProyecto.py')

    

    #PRIMER PASO : me descargo los videos de cloudinary y les cambio el nombre para ello tengo que hacer un get
    responseFrontal = requests.get(videoFrontal)

    
    with open('videos/frontal.mp4', 'wb') as f:
        f.write(responseFrontal.content)

    responsePerfil = requests.get(videoPerfil)
    with open('videos/perfil.mp4', 'wb') as f:
        f.write(responsePerfil.content)

    time.sleep(40)


    #SEGUNDO PASO : los subo a google drive
    os.system('python subirVideoDrive.py')


    #TERCER PASO: esperamos unos 40 segundos para asegurarnos de que se ha subido correctamente
    time.sleep(40)
    print("espera finalizada")


    #CUARTO PASO:  accedo a Flask con el /openPose (el resto del enlace es dinamico). Cuando se termine el get, ya tenemos los keypoint guardados en google drive

    url = config.URL + "/openPose"

    # Realizar la solicitud GET
    try:
        response = requests.get(url)
        response.raise_for_status()
        print("Get realizado ")

        # Verificar el código de estado de la respuesta
        if response.status_code == 200:
            print("Solicitud realizada correctamente")
        else:
            print("La solicitud no se pudo completar. Código de estado:", response.status_code)


        time.sleep(40)

        #QUINTO PASO : descargar de Google Drive los keyPoints
        os.system('python descargarGoogleDrive.py')

        #SEXTO PASO : Analizar los datos dependiendo del movimiento que es (REALMENTE DEPENDE DEL ARRAY DE TIPS)
        url= "http://localhost:8001/ejercicios/filter/"+ idEjercicio
        response = requests.get(url)
        if response.status_code == 200:
            ejercicio = response.json() 
            print(ejercicio)
        else:
            print("La solicitud no se pudo completar. Código de estado:", response.status_code)


        #con esto tenemos el numero de archivos, para ver sobre cuantos keypoints comprobamos
        #tambien tenemos los archivos en forma de array
        dir_path = 'InfoOpenPose/json/frontalJson'
        filesFrontal = os.listdir(dir_path)
        keypointsFrontal= len(filesFrontal)
        dir_path = 'InfoOpenPose/json/perfilJson'
        filesPerfil = os.listdir(dir_path)
        keypointsPerfil= len(filesPerfil)
        correcto = []
        incorrecto= []


        #EVALUAREMOS PARA CADA TIPO DE DICHO EJERCICIO : 

        for tip in ejercicio['tips'] :

            if tip == "ANCHURAPIESCADERA" :    #frontal
                contador= 0 
                secumple= 0
                muyancho=0
                muycerrado=0
                cotaSuperior=85
                cotaInferior=16

                while contador < len(filesFrontal) * 0.5 :
                    archivo_json= 'InfoOpenPose/json/frontalJson/' + filesFrontal[contador]
                    perfil_pose_keypoints_2d = extract_pose_keypoints_2d(archivo_json)

                    caderaDer_x=perfil_pose_keypoints_2d[9*3]
                    caderaIzq_x=perfil_pose_keypoints_2d[12*3]
                    tobilloDer_x=perfil_pose_keypoints_2d[11*3]
                    tobilloIzq_x=perfil_pose_keypoints_2d[14*3]

                    diferenciaIzquierda =abs(tobilloIzq_x - caderaIzq_x)
                    diferenciaDerecha = abs(tobilloDer_x -caderaDer_x)


                    if diferenciaIzquierda >=cotaSuperior and diferenciaDerecha >= cotaSuperior :
                        muyancho = muyancho+1 
                    elif(diferenciaIzquierda <= cotaInferior and diferenciaIzquierda<= cotaInferior):
                        muycerrado=muycerrado+1 
                    else:
                        secumple = secumple+1

                    contador = contador +1
                            
                if secumple > (0.55* contador):
                    correcto.append("Anchura de los pies correcta")
                elif muycerrado >= (0.55*contador): 
                    incorrecto.append("La anchura de los pies debe ser más abierta. Separe más los pies.")
                elif muyancho >= (0.55*contador):
                    incorrecto.append("La anchura de los pies debe ser más cerrada. Junte más los pies.")
    

            if tip == "ANCHURAABIERTOAGARREBARRA" : # frontal
                contador=0
                secumple=0
                cierraAgarre=0
                abreAgarre=0
                cotaInferior = 145 #181
                cotaSuperior = 370

                while(contador < len(filesFrontal) * 0.5) :
                    archivo_json= 'InfoOpenPose/json/frontalJson/' + filesFrontal[contador]
                    perfil_pose_keypoints_2d = extract_pose_keypoints_2d(archivo_json)
                    muñecaDer_x=perfil_pose_keypoints_2d[4*3]
                    muñecaIzq_x=perfil_pose_keypoints_2d[7*3]
                    hombroDer_x = perfil_pose_keypoints_2d[2*3]
                    hombroIzq_x = perfil_pose_keypoints_2d[5*3]

                    diferenciaDerecha= hombroDer_x-muñecaDer_x
                    diferenciaIzquierda= muñecaIzq_x-hombroIzq_x 

                 
                    secumpleCierraAgarre=False
                    secumpleAbreAgarre=False



                    if(diferenciaDerecha > cotaSuperior and (diferenciaIzquierda > cotaSuperior)) :
                        cierraAgarre= cierraAgarre+1
                        secumpleCierraAgarre = True
                    if( diferenciaDerecha < cotaInferior and (diferenciaIzquierda < cotaInferior )):
                        abreAgarre = abreAgarre +1
                        secumpleAbreAgarre = True

                    if(secumpleCierraAgarre == False and secumpleAbreAgarre== False) : # se cumple si los dos son falsos
                        secumple = secumple+1

                    contador=contador + 1
                                                        
                if(secumple >= 0.55 * contador) :
                    correcto.append("Agarre ancho ")
                elif(cierraAgarre > 0.55 * contador):
                                incorrecto.append("Agarre demasiado abierto, junte más las manos")
                elif(abreAgarre > 0.55 *contador):
                                incorrecto.append("Agarre demasiado cerrado, separe más las manos")     
                                               
                                    


            elif tip == "ANCHURACERRADOAGARREBARRA": 
                contador=0
                secumple=0
                cierraAgarre=0
                abreAgarre=0
                cotaInferior = 47
                cotaSuperior =145  #180

                while(contador < len(filesFrontal) * 0.5) :
                    archivo_json= 'InfoOpenPose/json/frontalJson/' + filesFrontal[contador]
                    perfil_pose_keypoints_2d = extract_pose_keypoints_2d(archivo_json)
                    muñecaDer_x=perfil_pose_keypoints_2d[4*3]
                    muñecaIzq_x=perfil_pose_keypoints_2d[7*3]
                    hombroDer_x = perfil_pose_keypoints_2d[2*3]
                    hombroIzq_x = perfil_pose_keypoints_2d[5*3]

                    diferenciaDerecha= hombroDer_x-muñecaDer_x
                    diferenciaIzquierda= muñecaIzq_x-hombroIzq_x 

                    secumpleCierraAgarre=False
                    secumpleAbreAgarre=False

                    if(diferenciaDerecha > cotaSuperior and (diferenciaIzquierda > cotaSuperior)) :
                        cierraAgarre= cierraAgarre+1
                        secumpleCierraAgarre = True
                    if( diferenciaDerecha < cotaInferior and (diferenciaIzquierda < cotaInferior )):
                        abreAgarre = abreAgarre +1
                        secumpleAbreAgarre = True

                    if(secumpleCierraAgarre == False and secumpleAbreAgarre== False) : # se cumple si los dos son falsos
                        secumple = secumple+1

                    contador=contador + 1
                                                        
                if(secumple >= 0.55 * contador) :
                    correcto.append("Agarre cerrado ")
                elif(cierraAgarre > 0.55 * contador):
                                incorrecto.append("Agarre demasiado abierto, junte más las manos")
                elif(abreAgarre > 0.55 *contador):
                                incorrecto.append("Agarre demasiado cerrado, separe más las manos")     



            elif tip == "BARRAPEGADACUERPO": #muñeca-talon(perfil, solo me intereesa el lado izquierdo)
                contador=0
                nopegada=0
                cota=135
                limiteveces= 10

                for keypoint in filesPerfil :
                    archivo_json= 'InfoOpenPose/json/perfilJson/' + keypoint
                    perfil_pose_keypoints_2d = extract_pose_keypoints_2d(archivo_json)

                    muñecaIzq_x=perfil_pose_keypoints_2d[7*3]
                    talonIzq_x=perfil_pose_keypoints_2d[21*3]
                    diferencia = abs(muñecaIzq_x-talonIzq_x) 

                    if( diferencia >  cota):
                        nopegada = nopegada+1

                if nopegada > limiteveces:
                    incorrecto.append("Manten la barra pegada a tu cuerpo durante todo el movimiento")
                else:
                    correcto.append("Barra pegada al cuerpo")   



            elif tip == "EXTENSIONCADERA": #
                caderafinal=0
                nelementos = len(filesPerfil)
                contador= int(0.75*nelementos)
                cotaExtensionCadera=16
                cota = 3 # numero de  veces que debe cumplirse la extension de cadera 

                    

                while (contador < nelementos) :
                    archivo_json= 'InfoOpenPose/json/perfilJson/' + filesPerfil[contador]
                    perfil_pose_keypoints_2d = extract_pose_keypoints_2d(archivo_json)

                    hombroIzq_x=perfil_pose_keypoints_2d[5*3]
                    caderaIzq_x=perfil_pose_keypoints_2d[12*3]

                    extCadera = caderaIzq_x-hombroIzq_x
                    print(extCadera)
                    
                    if( extCadera <= cotaExtensionCadera) :
                        caderafinal = caderafinal+1
                    contador = contador+1


                if(caderafinal >=cota )  :
                    correcto.append("Extensión de cadera.") 
                else:
                    incorrecto.append("Debe extender la cadera, es decir" + "\n" + " tu hombro debe quedar a la altura de tu cadera.")




            elif tip == "EXTENSIONRODILLAS":
                rodillafinal=0
                nelementos = len(filesPerfil)
                contador= int(0.75*nelementos)
                cotaExtensionRodilla=86
                cota =3 # numero de  vecesque debe cumplirse la extension de rodillas

                    

                while (contador < nelementos) :
                    archivo_json= 'InfoOpenPose/json/perfilJson/' + filesPerfil[contador]
                    perfil_pose_keypoints_2d = extract_pose_keypoints_2d(archivo_json)

                    rodillaIzq_x=perfil_pose_keypoints_2d[13*3]
                    talonIzq_x=perfil_pose_keypoints_2d[21*3]

                    extRodilla = talonIzq_x- rodillaIzq_x
                    
                    if( extRodilla <= cotaExtensionRodilla) :
                        rodillafinal = rodillafinal+1
                    contador = contador+1


                if(rodillafinal >=cota )  :
                    correcto.append("Extensión de rodilla. ") 
                else:
                    incorrecto.append("Debe extender la rodilla.")



            elif tip == "BARRASUBEVERTICALMENTE": #codo-muñeca, perfil
              
                margen=10 # margen de error
                limiteVeces= 5
                contador = 0 
                contador2= 0
                while(contador2 < 0.8* keypointsPerfil) :

                    archivo_json= 'InfoOpenPose/json/perfilJson/' + filesPerfil[contador2]
                    perfil_pose_keypoints_2d = extract_pose_keypoints_2d(archivo_json)
                                        
                    muñecaIzq_x=perfil_pose_keypoints_2d[7*3]
                    codoIzq_x=perfil_pose_keypoints_2d[6*3]
                            

                    diferencia= muñecaIzq_x-codoIzq_x
                    print(diferencia)
                    if(diferencia + margen  < 0) :# si la diferencia + la cota es negativa es porque la muñeca está adelantando al codo
                        contador = contador+1
                    contador2= contador2+1
                                        

                if contador >= limiteVeces :
                    incorrecto.append("La barra debe subir lo más vertical posible. "   + "\n" +  "La mano no debe adelantar al codo en ningún momento")
                else:
                    correcto.append("La barra sube de forma vertical")




            
            elif tip == "RODILLASSIGUENLINEAPIES": # rodillas-bigtoes frontal eje x
                contador=int(0.32*keypointsFrontal)
                limiteVeces=5
                rodillasFuera= 0
                rodillasDentro= 0
                margen = 3

                while (contador < int(0.73*keypointsFrontal)) :
                    archivo_json= 'InfoOpenPose/json/frontalJson/' + filesFrontal[contador]
                    perfil_pose_keypoints_2d = extract_pose_keypoints_2d(archivo_json)

                    rodillaDer_x=perfil_pose_keypoints_2d[10*3]
                    rodillaIzq_x=perfil_pose_keypoints_2d[13*3]
                    bigToeDer_x=perfil_pose_keypoints_2d[22*3]
                    bigToeIzq_x=perfil_pose_keypoints_2d[19*3]
                    talon_Izq_x =perfil_pose_keypoints_2d[21*3]
                    talon_Der_x =perfil_pose_keypoints_2d[24*3]


                    if((talon_Der_x-rodillaDer_x <= (-5) )and (rodillaIzq_x-talon_Izq_x <= (-5) )) :
                            rodillasDentro =rodillasDentro +1 

                    if((rodillaDer_x-bigToeDer_x <= (-52) ) and ( bigToeIzq_x - rodillaIzq_x <=  (-52) )) : 
                        rodillasFuera= rodillasFuera +1

                    contador=contador+1


                if rodillasFuera >= limiteVeces:
                    incorrecto.append("Evite llevar las rodillas hacia fuera. "  + "\n" + " Intente que las rodillas sigan la línea del pie")
                elif rodillasDentro >= limiteVeces : 
                    incorrecto.append("Evite llevar las rodillas hacia dentro. "   + "\n" + " Intente que las rodillas sigan la línea del pie")
                else:
                    correcto.append("Las rodillas siguen la línea del pie correctamente")






            elif tip == "ROMPERELPARALELO": #cadera-rodilla(eje y) (perfil, solo me interesa lado izquierdo)
                limiteVeces=3
                contador=0

                for keypoint in filesPerfil :
                    archivo_json= 'InfoOpenPose/json/perfilJson/' + keypoint
                    perfil_pose_keypoints_2d = extract_pose_keypoints_2d(archivo_json)

                    rodillaIzq_y=perfil_pose_keypoints_2d[13*3+1]
                    caderaIzq_y=perfil_pose_keypoints_2d[12*3+1]

                    diferencia = rodillaIzq_y-caderaIzq_y


                    if(diferencia < 0) : # si es menor que 0 está rompiendo el paralelo
                        contador = contador +1
                            

                if(contador >= limiteVeces):
                    correcto.append("Está rompiendo el paralelo correctamente")
                else:
                    incorrecto.append("Baje más profundo, no está rompiendo el paralelo")



            elif tip == "CODOSALTOSPOSICIONFRONTRACK": # perfil, codos-hombros eje y
                limiteVeces=4 
                contador = 0 
                margendedistancia=54
                contador2 = 0

                while(contador2 < 0.3*keypointsPerfil):

                    archivo_json= 'InfoOpenPose/json/perfilJson/' + filesPerfil[contador2]
                    perfil_pose_keypoints_2d = extract_pose_keypoints_2d(archivo_json)
                    hombroIzq_x=perfil_pose_keypoints_2d[5*3]
                    codoIzq_x=perfil_pose_keypoints_2d[6*3]
                    diferencia= abs(codoIzq_x-hombroIzq_x)


                    if(diferencia <= margendedistancia) :
                        contador = contador+1
                    contador2= contador2 +1
                                        
                if(contador >= limiteVeces):
                    incorrecto.append("Recuerde llevar los codos altos en posición de Front Rack")
                else:
                    correcto.append("Codos altos en posición de Front Rack")

  
            elif tip== "EXTENSIONCOMPLETACODOS": # muñeca, hombro, codos, frontal ejes xy
                margen = 44
                contador = int(0.75* keypointsFrontal)
                secumple=0
                limiteVeces=3


                while(contador < keypointsFrontal):
                    archivo_json= 'InfoOpenPose/json/frontalJson/' + filesFrontal[contador]
                    perfil_pose_keypoints_2d = extract_pose_keypoints_2d(archivo_json)

                    hombroIzq_x=perfil_pose_keypoints_2d[5*3]
                    hombroIzq_y=perfil_pose_keypoints_2d[5*3+1]
                    codoIzq_x=perfil_pose_keypoints_2d[6*3]
                    codoIzq_y=perfil_pose_keypoints_2d[6*3+1]
                    muñecaIzq_x=perfil_pose_keypoints_2d[7*3]
                    muñecaIzq_y=perfil_pose_keypoints_2d[7*3+1]
                    hombroDer_x =perfil_pose_keypoints_2d[2*3]
                    hombroDer_y =perfil_pose_keypoints_2d[2*3+1]
                    codoDer_x= perfil_pose_keypoints_2d[3*3]
                    codoDer_y= perfil_pose_keypoints_2d[3*3+1]
                    muñecaDer_x=perfil_pose_keypoints_2d[4*3]
                    muñecaDer_y=perfil_pose_keypoints_2d[4*3+1]

                    # para lado izquierdo :
                    m1 = (muñecaIzq_y - hombroIzq_y) / (muñecaIzq_x - hombroIzq_x)
                    n1 = muñecaIzq_y - m1 * muñecaIzq_x
                    supuestoValorCodoIzquierdo= m1 * codoIzq_x + n1
                    valorCodoIzquierdo=codoIzq_y

                    m2 = (muñecaDer_y - hombroDer_y) / (muñecaDer_x - hombroDer_x)
                    n2 = muñecaDer_y - m2 * muñecaDer_x
                    supuestoValorCodoDerecho= m2 * codoDer_x + n2
                    valorCodoDerecho= codoDer_y


                    if(abs(supuestoValorCodoIzquierdo-valorCodoIzquierdo) < margen and abs(supuestoValorCodoDerecho-valorCodoDerecho) < margen) :
                        secumple= secumple+1

                    contador = contador +1

                if(secumple >= limiteVeces):
                    correcto.append("Extensión de codos.")
                else: 
                    incorrecto.append("Extienda los codos, es decir, estire los brazos al completo")


        
            elif tip== "SACARCABEZA" : #perfil, oreja,codo eje x
                contador = int(0.6* len(filesPerfil))
                secumple=0
                limiteVeces=2

                while(contador < len(filesPerfil)):
                    archivo_json= 'InfoOpenPose/json/perfilJson/' + filesPerfil[contador]
                    perfil_pose_keypoints_2d = extract_pose_keypoints_2d(archivo_json)


                    codoIzq_x=perfil_pose_keypoints_2d[6*3]
                    oidoIzq_x=perfil_pose_keypoints_2d[18*3]
                    diferencia= codoIzq_x -  oidoIzq_x

                    if(diferencia >= 0) :
                        secumple=secumple+1
                    contador= contador+1

                if(secumple>=limiteVeces) :
                    correcto.append("Barra queda detrás de la cabeza")
                else:
                    incorrecto.append("La barra debe quedar ligeramente por detrás de tu cabeza, es decir, "   + "\n" +  " los hombros deben quedar por detrás de las orejas")






            elif tip == "MANTENERESPALDARECTADESDESUELO": #cadera-hombro eje y perfil
                contador=0
                margen=85
                limiteVeces=5


                for keypoint in filesPerfil :
                    archivo_json= 'InfoOpenPose/json/perfilJson/' + keypoint
                    perfil_pose_keypoints_2d = extract_pose_keypoints_2d(archivo_json)

                    hombroIzq_y=perfil_pose_keypoints_2d[5*3+1]
                    caderaIzq_y=perfil_pose_keypoints_2d[12*3+1]
                    diferencia = abs(caderaIzq_y-hombroIzq_y)

                    if(diferencia < margen) :
                        contador = contador +1
                    

                if(contador >= limiteVeces) :
                    incorrecto.append("Mantenga la espalda recta. Para ello piense en sacar pecho "   + "\n" + "   y mirar al frente mientras realiza el movimiento")
                else:
                    correcto.append("Espalda recta durante todo el movimiento")                
                            



            elif tip == "MANTENERESPALDARECTADESDENOSUELO": #cadera-hombro eje y perfil
                contador=0
                margen=130
                limiteVeces=5


                for keypoint in filesPerfil :
                    archivo_json= 'InfoOpenPose/json/perfilJson/' + keypoint
                    perfil_pose_keypoints_2d = extract_pose_keypoints_2d(archivo_json)

                    hombroIzq_y=perfil_pose_keypoints_2d[5*3+1]
                    caderaIzq_y=perfil_pose_keypoints_2d[12*3+1]
                    diferencia = abs(caderaIzq_y-hombroIzq_y)

                    if(diferencia < margen) :
                        contador = contador +1
                    


                if(contador >= limiteVeces) :
                    incorrecto.append("Mantenga la espalda recta. Para ello piense en sacar pecho  "   + "\n" + " y mirar al frente mientras realiza el movimiento")
                else:
                    correcto.append("Espalda recta durante todo el movimiento")                
                                        



            
        
        #SEPTIMO PASO : generamos un informe  en formato pdf y le mandamos un correo con el informe
        informe = generarInforme(correcto,incorrecto)

        destinatario = emailUsuario
        asunto = 'Funcional Training Assistance'
        mensaje_texto = '¡Ya está disponible tu informe generado por Functional Training Assistance!'
        archivo_adjunto = 'informe.pdf'
        enviar_correo(destinatario, asunto, mensaje_texto, archivo_adjunto)
    except requests.exceptions.RequestException as e:
        print("Error al ejecutar OpenPose:", e)
        destinatario = emailUsuario
        asunto = 'Funcional Training Assistance'
        mensaje_texto = '¡Error al generar tu informe, vuelva a intentarlo!'
        generarInformeError()
        archivo_adjunto = 'informe.pdf'
        enviar_correo(emailUsuario,asunto,mensaje_texto,archivo_adjunto)
        print("")



    return informe


def generarInformeError() : 
    informe = "Error en el servidor al generar el informe, vuelva a intentarlo"

    c = canvas.Canvas("informe.pdf")
    c.setFont("Helvetica", 14)
    y = 750
    for line in informe.splitlines():
        c.drawString(100, y, line)
        y -= 20
    c.save()
    return informe



def generarInforme(correcto, incorrecto):
    informe = "INFORME GENERADO \n"
    informe += "REALIZADO CORRECTAMENTE: \n"

    for t in correcto:
        informe += "-" + t + "\n"

    informe = informe + "\n"
    informe += "ASPECTOS A MEJORAR: \n"

    for t in incorrecto:
        informe += "-" + t + "\n"

    c = canvas.Canvas("informe.pdf")
    c.setFont("Helvetica", 14)
    y = 750
    for line in informe.splitlines():
        c.drawString(100, y, line)
        y -= 20
    c.save()
    return informe






def enviar_correo(destinatario, asunto, mensaje_texto, archivo_adjunto):
    # Credenciales y token de acceso
    token = 'token.json'

    # Configuración de alcance y autorización de OAuth 2.0 + g drive
    SCOPES= ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/drive.file','https://www.googleapis.com/auth/gmail.send']

    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())


    # Crear el servicio de la API de Gmail
    service = build('gmail', 'v1', credentials=creds)

    # Crear el mensaje MIME
    mensaje = MIMEMultipart()
    mensaje['to'] = destinatario
    mensaje['subject'] = asunto

    # Adjuntar el mensaje de texto
    mensaje.attach(MIMEText(mensaje_texto, 'plain'))

    # Adjuntar el archivo PDF
    adjunto = MIMEBase('application', 'octet-stream')
    adjunto.set_payload(open(archivo_adjunto, 'rb').read())
    encoders.encode_base64(adjunto)
    adjunto.add_header('Content-Disposition', f'attachment; filename={archivo_adjunto}')
    mensaje.attach(adjunto)

    # Enviar el correo electrónico
    mensaje_raw = base64.urlsafe_b64encode(mensaje.as_bytes()).decode('utf-8')
    service.users().messages().send(userId='me', body={'raw': mensaje_raw}).execute()

    print('Correo electrónico enviado con éxito.')

