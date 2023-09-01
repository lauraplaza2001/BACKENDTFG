import os
import json

def extract_pose_keypoints_2d(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data['people'][0]['pose_keypoints_2d']


dir_path = './InfoOpenPose/json/frontalJson'
filesFrontal = os.listdir(dir_path)
keypointsFrontal= len(filesFrontal)
dir_path = './InfoOpenPose/json/perfilJson'
filesPerfil = os.listdir(dir_path)
keypointsPerfil= len(filesPerfil)
correcto = []
incorrecto= []



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
                #   rodillaDer_x=perfil_pose_keypoints_2d[10*3]
                #  rodillaIzq_x=perfil_pose_keypoints_2d[13*3]

    diferenciaDerecha= hombroDer_x-muñecaDer_x
    diferenciaIzquierda= muñecaIzq_x-hombroIzq_x 

    print(diferenciaIzquierda)
    print(diferenciaDerecha)
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
                                
print(secumple)    
print(abreAgarre)
print(cierraAgarre)        
    


print(correcto)
print(incorrecto)




