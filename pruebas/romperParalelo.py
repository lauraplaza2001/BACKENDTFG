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


limiteVeces=3
contador=0


for keypoint in filesPerfil :
    archivo_json= 'InfoOpenPose/json/perfilJson/' + keypoint
    perfil_pose_keypoints_2d = extract_pose_keypoints_2d(archivo_json)

    rodillaIzq_y=perfil_pose_keypoints_2d[13*3+1]
    caderaIzq_y=perfil_pose_keypoints_2d[12*3+1]

    diferencia = rodillaIzq_y-caderaIzq_y
    print(diferencia)


    if(diferencia < 0) : # si es menor que 0 está rompiendo el paralelo
        contador = contador +1
                            

if(contador >= limiteVeces):
    correcto.append("Está rompiendo el paralelo correctamente")
else:
    incorrecto.append("Baje más profundo, no está rompiendo el paralelo")

print(contador)


print(correcto)
print(incorrecto)










