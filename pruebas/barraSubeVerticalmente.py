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





margen=10 # margen de error
limiteVeces= 5
contador = 0 
contador2= 0
while(contador2 < 0.8* keypointsPerfil) :

    archivo_json= './InfoOpenPose/json/perfilJson/' + filesPerfil[contador2]
    perfil_pose_keypoints_2d = extract_pose_keypoints_2d(archivo_json)
                                        
    muñecaIzq_x=perfil_pose_keypoints_2d[7*3]
    codoIzq_x=perfil_pose_keypoints_2d[6*3]
                            
    diferencia= muñecaIzq_x-codoIzq_x
    print(diferencia)
    if(diferencia + margen  < 0) :# si la diferencia + la cota me sale negativo es porque la muñeca está adelantando al codo
        contador = contador+1
    contador2= contador2+1
                                        

if contador >= limiteVeces :
    incorrecto.append("La barra debe subir lo más vertical posible. La mano no debe adelantar al codo en ningún momento")
else:
    correcto.append("La barra sube de forma vertical")

print(contador)


print(correcto)
print(incorrecto)










