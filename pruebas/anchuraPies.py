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


contador= 0 
secumple= 0
muyancho=0
muycerrado=0
cotaSuperior=85
cotaInferior=16

while contador < len(filesFrontal) * 0.5 :
    archivo_json= './InfoOpenPose/json/frontalJson/' + filesFrontal[contador]
    perfil_pose_keypoints_2d = extract_pose_keypoints_2d(archivo_json)

    caderaDer_x=perfil_pose_keypoints_2d[9*3]
    caderaIzq_x=perfil_pose_keypoints_2d[12*3]
    tobilloDer_x=perfil_pose_keypoints_2d[11*3]
    tobilloIzq_x=perfil_pose_keypoints_2d[14*3]

    diferenciaIzquierda =abs(tobilloIzq_x - caderaIzq_x)
    diferenciaDerecha = abs(tobilloDer_x -caderaDer_x)
    print(diferenciaDerecha)
    print(diferenciaIzquierda)


    if diferenciaIzquierda >=cotaSuperior and diferenciaDerecha >= cotaSuperior :
        muyancho = muyancho+1 
    elif(diferenciaIzquierda <= cotaInferior and diferenciaIzquierda<= cotaInferior):
        muycerrado=muycerrado+1 
    else:
        secumple = secumple+1

    contador = contador +1
                            
if secumple > (0.55* contador):
    correcto.append("Anchura de los pies correcta")
elif muycerrado >= (0.55*contador): 
    incorrecto.append("La anchura de los pies debe ser más abierta. Separe más los pies.")
elif muyancho >= (0.55*contador):
    incorrecto.append("La anchura de los pies debe ser más cerrada. Junte más los pies.")
               
print(muycerrado)
print(muyancho)

print(correcto)
print(incorrecto)







