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



margen = 44
contador = int(0.75* keypointsFrontal)
secumple=0
limiteVeces=3


while(contador < keypointsFrontal):
    archivo_json= './InfoOpenPose/json/frontalJson/' + filesFrontal[contador]
    perfil_pose_keypoints_2d = extract_pose_keypoints_2d(archivo_json)

    hombroIzq_x=perfil_pose_keypoints_2d[5*3]
    hombroIzq_y=perfil_pose_keypoints_2d[5*3+1]
    codoIzq_x=perfil_pose_keypoints_2d[6*3]
    codoIzq_y=perfil_pose_keypoints_2d[6*3+1]
    muñecaIzq_x=perfil_pose_keypoints_2d[7*3]
    muñecaIzq_y=perfil_pose_keypoints_2d[7*3+1]
    hombroDer_x =perfil_pose_keypoints_2d[2*3]
    hombroDer_y =perfil_pose_keypoints_2d[2*3+1]
    codoDer_x= perfil_pose_keypoints_2d[3*3]
    codoDer_y= perfil_pose_keypoints_2d[3*3+1]
    muñecaDer_x=perfil_pose_keypoints_2d[4*3]
    muñecaDer_y=perfil_pose_keypoints_2d[4*3+1]

                    # para lado izquierdo :
                                
    m1 = (muñecaIzq_y - hombroIzq_y) / (muñecaIzq_x - hombroIzq_x)
    n1 = muñecaIzq_y - m1 * muñecaIzq_x
    supuestoValorCodoIzquierdo= m1 * codoIzq_x + n1
    valorCodoIzquierdo=codoIzq_y

    m2 = (muñecaDer_y - hombroDer_y) / (muñecaDer_x - hombroDer_x)
    n2 = muñecaDer_y - m2 * muñecaDer_x
    supuestoValorCodoDerecho= m2 * codoDer_x + n2
    valorCodoDerecho= codoDer_y

    print("Derecha: diferencia)")
    print(abs(supuestoValorCodoDerecho-valorCodoDerecho))
                

    print("Izquierda:(supuesto valor + valor Real)")
    print(abs(supuestoValorCodoIzquierdo-valorCodoIzquierdo))

    if(abs(supuestoValorCodoIzquierdo-valorCodoIzquierdo) < margen and abs(supuestoValorCodoDerecho-valorCodoDerecho) < margen) :
        secumple= secumple+1

    contador = contador +1

if(secumple >= limiteVeces):
    correcto.append("Extensión de codos al final del movimiento")
else: 
    incorrecto.append("Extienda los codos al final del movimiento")
    
print(secumple)


#-----------------------------
print(correcto)
print(incorrecto)




