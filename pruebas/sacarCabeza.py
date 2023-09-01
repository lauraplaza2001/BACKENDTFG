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



contador = int(0.6* len(filesPerfil))
secumple=0
limiteVeces=2

while(contador < len(filesPerfil)):
    archivo_json= './InfoOpenPose/json/perfilJson/' + filesPerfil[contador]
    perfil_pose_keypoints_2d = extract_pose_keypoints_2d(archivo_json)


    codoIzq_x=perfil_pose_keypoints_2d[6*3]
    oidoIzq_x=perfil_pose_keypoints_2d[18*3]
    diferencia= codoIzq_x -  oidoIzq_x
    print(diferencia)

    if(diferencia >= 0) :
        secumple=secumple+1
    contador= contador+1

if(secumple>=limiteVeces) :
    correcto.append("Barra queda detrás de la cabeza")
else:
    incorrecto.append("La barra debe quedar ligeramente por detrás de tu cabeza, es decir, los hombros deben quedar por detrás de las orejas")


print(secumple)

print(correcto)
print(incorrecto)










