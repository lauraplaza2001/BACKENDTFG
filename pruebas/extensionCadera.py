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

caderafinal=0
nelementos = len(filesPerfil)
contador= int(0.75*nelementos)
cotaExtensionCadera=16
cota = 3 # numero de  vecesque debe cumplirse la extension de cadera 

                  

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
    correcto.append("Extensión de cadera final") 
else:
    incorrecto.append("Debe extender la cadera al final del movimiento, es decir, tu hombro debe quedar a la altura de tu cadera.")


print(caderafinal)
print(correcto)
print(incorrecto)






