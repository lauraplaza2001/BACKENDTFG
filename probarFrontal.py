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

contador=int(0.2*keypointsFrontal)
limiteVeces=3
rodillasFuera= 0
rodillasDentro= 0
margen = 3

while (contador < int(0.8*keypointsFrontal)) :
    archivo_json= 'InfoOpenPose/json/frontalJson/' + filesFrontal[contador]
    perfil_pose_keypoints_2d = extract_pose_keypoints_2d(archivo_json)

    rodillaDer_x=perfil_pose_keypoints_2d[10*3]
    rodillaIzq_x=perfil_pose_keypoints_2d[13*3]
    bigToeDer_x=perfil_pose_keypoints_2d[22*3]
    bigToeIzq_x=perfil_pose_keypoints_2d[19*3]
    caderaDer_x=perfil_pose_keypoints_2d[9*3]
    caderaIzq_x=perfil_pose_keypoints_2d[12*3]

    difCaderas= abs(caderaDer_x-caderaIzq_x)
    difRodillas=abs(rodillaDer_x-rodillaIzq_x)
    print("cadera")            
    diferenciaDer= caderaDer_x-rodillaDer_x
    diferenciaIzq= rodillaIzq_x - caderaIzq_x
  #  print(int(diferenciaDer))
   # print(int(diferenciaIzq))
    print(difCaderas)
    print("rodillas")
    print(difRodillas)

    if(difRodillas >= 3.3*difCaderas) :
        rodillasFuera = rodillasFuera+1
    elif(difRodillas <= 1.5* difCaderas):
        rodillasDentro = rodillasDentro +1

  

    contador=contador+1

print(rodillasFuera)
print(rodillasDentro)

if rodillasFuera >= limiteVeces:
    incorrecto.append("Evite llevar las rodillas hacia fuera. Intente que las rodillas sigan la línea del pie")
elif rodillasDentro >= limiteVeces : 
    incorrecto.append("Evite llevar las rodillas hacia dentro. Intente que las rodillas sigan la línea del pie")
else:
    correcto.append("Las rodillas siguen la línea del pie correctamente")



print(correcto)
print(incorrecto)