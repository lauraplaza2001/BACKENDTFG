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
#------- CODIGO A MODIFICAR PARA PROBAR TIPS ----------

contador=0
nopegada=0
cota=135
limiteveces= 10

for keypoint in filesPerfil :
    archivo_json= './InfoOpenPose/json/perfilJson/' + keypoint
    perfil_pose_keypoints_2d = extract_pose_keypoints_2d(archivo_json)

    muñecaIzq_x=perfil_pose_keypoints_2d[7*3]
    talonIzq_x=perfil_pose_keypoints_2d[21*3]
    diferencia = abs(muñecaIzq_x-talonIzq_x) 
    print(diferencia)

    if( diferencia >  cota):
        nopegada = nopegada+1

if nopegada > limiteveces:
    incorrecto.append("Manten la barra pegada a tu cuerpo durante todo el movimiento")
else:
    correcto.append("Barra pegada al cuerpo")   

print(nopegada)
print(keypointsPerfil)
#-----------------------------
print(correcto)
print(incorrecto)




