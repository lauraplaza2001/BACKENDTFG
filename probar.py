import os
import json

def extract_pose_keypoints_2d(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data['people'][0]['pose_keypoints_2d']


dir_path = 'InfoOpenPose/json/frontalJson'
filesFrontal = os.listdir(dir_path)
keypointsFrontal= len(filesFrontal)
dir_path = 'InfoOpenPose/json/perfilJson'
filesPerfil = os.listdir(dir_path)
keypointsPerfil= len(filesPerfil)
correcto = []
incorrecto= []



print("Vamos  por anchura pies cadera")


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
