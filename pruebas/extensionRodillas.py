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



rodillafinal=0
nelementos = len(filesPerfil)
contador= int(0.75*nelementos)
cotaExtensionRodilla=86
cota =3 # numero de  vecesque debe cumplirse la extension de rodillas

                    

while (contador < nelementos) :
    archivo_json= 'InfoOpenPose/json/perfilJson/' + filesPerfil[contador]
    perfil_pose_keypoints_2d = extract_pose_keypoints_2d(archivo_json)

    rodillaIzq_x=perfil_pose_keypoints_2d[13*3]
    talonIzq_x=perfil_pose_keypoints_2d[21*3]

    extRodilla = talonIzq_x- rodillaIzq_x
    print(extRodilla)
                    
    if( extRodilla <= cotaExtensionRodilla) :
        rodillafinal = rodillafinal+1
    contador = contador+1


if(rodillafinal >=cota )  :
    correcto.append("Extensión de rodilla final") 
else:
    incorrecto.append("Debe extender la rodilla al final del movimiento")

print(rodillafinal)
#-----------------------------
print(correcto)
print(incorrecto)




