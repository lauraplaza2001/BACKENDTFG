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

pesoPuntillas=0
pesoTalones=0
cotaTalon = -8 # +- para que no se considere que se cumple
cotaPuntillas= 21
limiteVeces=4 # cuantas veces debe ocurrir para

for keypoint in filesFrontal :
    archivo_json= '../InfoOpenPose/json/frontalJson/' + keypoint
    perfil_pose_keypoints_2d = extract_pose_keypoints_2d(archivo_json)

    talonIzq_y=perfil_pose_keypoints_2d[21*3+1]
    bigToeIzq_y=perfil_pose_keypoints_2d[19*3+1]

    diferencia= bigToeIzq_y-talonIzq_y
    print(diferencia)

    if(diferencia > cotaPuntillas) :
        pesoPuntillas= pesoPuntillas+1 
    if(diferencia < cotaTalon) :
        pesoTalones= pesoTalones+1
                  
print(pesoPuntillas)
print(pesoTalones)        
                
if (pesoPuntillas > limiteVeces) :
    incorrecto.append("Apoye el talón durante todo el movimiento")
elif (pesoTalones > limiteVeces):
    incorrecto.append("Apoye la punta de los pies durante todo el movimiento")
else:
    correcto.append("Peso bien distribuido en los pies")



#-----------------------------
print(correcto)
print(incorrecto)







