import os
import json

def extract_pose_keypoints_2d(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data['people'][0]['pose_keypoints_2d']


dir_path = '../InfoOpenPose/json/frontalJson'
filesFrontal = os.listdir(dir_path)
keypointsFrontal= len(filesFrontal)
dir_path = '../InfoOpenPose/json/perfilJson'
filesPerfil = os.listdir(dir_path)
keypointsPerfil= len(filesPerfil)
correcto = []
incorrecto= []
#------- CODIGO A MODIFICAR PARA PROBAR TIPS ----------





contador=0
margen=130
limiteVeces=5


for keypoint in filesPerfil :
    archivo_json= '../InfoOpenPose/json/perfilJson/' + keypoint
    perfil_pose_keypoints_2d = extract_pose_keypoints_2d(archivo_json)

    hombroIzq_y=perfil_pose_keypoints_2d[5*3+1]
    caderaIzq_y=perfil_pose_keypoints_2d[12*3+1]
    diferencia = abs(caderaIzq_y-hombroIzq_y)
    print(diferencia)

    if(diferencia < margen) :
        contador = contador +1
                


if(contador >= limiteVeces) :
    incorrecto.append("Mantenga la espalda recta. Para ello piense en sacar pecho y mirar al frente mientras realiza el movimiento")
else:
    correcto.append("Espalda recta durante todo el movimiento")                
                        

print(contador)
#-----------------------------
print(correcto)
print(incorrecto)







