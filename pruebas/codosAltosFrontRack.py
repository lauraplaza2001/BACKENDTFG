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



limiteVeces=4 # si ocurre al menos 4 veces que los codos están mas bajos de la cuenta, entonces, esta mal
contador = 0 
margendedistancia=54
contador2 = 0

while(contador2 < 0.3*keypointsPerfil):

    archivo_json= './InfoOpenPose/json/perfilJson/' + filesPerfil[contador2]
    perfil_pose_keypoints_2d = extract_pose_keypoints_2d(archivo_json)
                                #solo el izquierdo
    hombroIzq_x=perfil_pose_keypoints_2d[5*3]
    codoIzq_x=perfil_pose_keypoints_2d[6*3]
    diferencia= abs(codoIzq_x-hombroIzq_x)
    print(diferencia)

    if(diferencia <= margendedistancia) :
        contador = contador+1
    contador2= contador2 +1
                                        
if(contador >= limiteVeces):
    incorrecto.append("Recuerde llevar los codos altos en posición de Front Rack")
else:
    correcto.append("Codos altos en posición de Front Rack")




print(contador)
#-----------------------------
print(correcto)
print(incorrecto)







