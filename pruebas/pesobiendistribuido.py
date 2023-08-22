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
contador=int(0.3*keypointsFrontal)
limiteVeces=7
rodillasFuera= 0
rodillasDentro= 0
margen = 3

while (contador < int(0.75*keypointsFrontal)) :
    archivo_json= '../InfoOpenPose/json/frontalJson/' + filesFrontal[contador]
    perfil_pose_keypoints_2d = extract_pose_keypoints_2d(archivo_json)

    rodillaDer_x=perfil_pose_keypoints_2d[10*3]
    rodillaIzq_x=perfil_pose_keypoints_2d[13*3]
    bigToeDer_x=perfil_pose_keypoints_2d[22*3]
    bigToeIzq_x=perfil_pose_keypoints_2d[19*3]
    talon_Izq_x =perfil_pose_keypoints_2d[21*3]
    talon_Der_x =perfil_pose_keypoints_2d[24*3]

  #  print("rodilla-bigtoe")

   # print(bigToeIzq_x- rodillaIzq_x)
    #print("talon-rodilla")
    print(talon_Der_x-rodillaDer_x)


#pongo primero rodillas dentro, pq rodillas fuera se confunde cuando los pies están muy abiertos
    if((talon_Der_x-rodillaDer_x <= (-5)) or (rodillaIzq_x-talon_Izq_x <= (-5) )) :
            rodillasDentro =rodillasDentro +1 

    elif((rodillaDer_x-bigToeDer_x <= (-5) ) or ( bigToeIzq_x - rodillaIzq_x<= (-5) )) : 
        rodillasFuera= rodillasFuera +1



    contador=contador+1



if rodillasFuera >= limiteVeces:
    incorrecto.append("Evite llevar las rodillas hacia fuera. Intente que las rodillas sigan la línea del pie")
elif rodillasDentro >= limiteVeces : 
    incorrecto.append("Evite llevar las rodillas hacia dentro. Intente que las rodillas sigan la línea del pie")
else:
    correcto.append("Las rodillas siguen la línea del pie correctamente")

print("rodillas dentro:")
print(rodillasDentro)
print("Rodillasfuera")
print(rodillasFuera)

#-----------------------------
print(correcto)
print(incorrecto)







