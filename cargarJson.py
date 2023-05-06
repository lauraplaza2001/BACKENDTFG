

import json

def extract_pose_keypoints_2d(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data['people'][0]['pose_keypoints_2d']



archivo_json = 'InfoOpenPose/json/frontalJson/frontal_000000000004_keypoints.json'
perfil_pose_keypoints_2d = extract_pose_keypoints_2d(archivo_json)
print(perfil_pose_keypoints_2d)



nariz_x =perfil_pose_keypoints_2d[0]
nariz_y = perfil_pose_keypoints_2d[1]
cuello_x = perfil_pose_keypoints_2d[1*3]
cuello_y = perfil_pose_keypoints_2d[1*3 +1]
hombroDer_x =perfil_pose_keypoints_2d[2*3]
hombroDer_y =perfil_pose_keypoints_2d[2*3+1]
codoDer_x= perfil_pose_keypoints_2d[3*3]
codoDer_y= perfil_pose_keypoints_2d[3*3+1]
muñecaDer_x=perfil_pose_keypoints_2d[4*3]
muñecaDer_y=perfil_pose_keypoints_2d[4*3+1]
hombroIzq_x=perfil_pose_keypoints_2d[5*3]
hombroIzq_y=perfil_pose_keypoints_2d[5*3+1]
codoIzq_x=perfil_pose_keypoints_2d[6*3]
codoIzq_y=perfil_pose_keypoints_2d[6*3+1]
muñecaIzq_x=perfil_pose_keypoints_2d[7*3]
muñecaIzq_y=perfil_pose_keypoints_2d[7*3+1]
caderaCentral_x=perfil_pose_keypoints_2d[8*3]
caderaCentral_y=perfil_pose_keypoints_2d[8*3+1]
caderaDer_x=perfil_pose_keypoints_2d[9*3]
caderaDer_y=perfil_pose_keypoints_2d[9*3+1]
rodillaDer_x=perfil_pose_keypoints_2d[10*3]
rodillaDer_y=perfil_pose_keypoints_2d[10*3+1]
tobilloDer_x=perfil_pose_keypoints_2d[11*3]
tobilloDer_y=perfil_pose_keypoints_2d[11*3+1]
caderaIzq_x=perfil_pose_keypoints_2d[12*3]
caderaIzq_y=perfil_pose_keypoints_2d[12*3+1]
rodillaIzq_x=perfil_pose_keypoints_2d[13*3]
rodillaIzq_y=perfil_pose_keypoints_2d[13*3+1]
tobilloIzq_x=perfil_pose_keypoints_2d[14*3]
tobilloIzq_y=perfil_pose_keypoints_2d[14*3+1]
ojoDer_x=perfil_pose_keypoints_2d[15*3]
ojoDer_y=perfil_pose_keypoints_2d[15*3+1]
ojoIzq_x=perfil_pose_keypoints_2d[16*3]
ojoIzq_y=perfil_pose_keypoints_2d[16*3+1]
oidoDer_x=perfil_pose_keypoints_2d[17*3]
oidoDer_y=perfil_pose_keypoints_2d[17*3+1]
oidoIzq_x=perfil_pose_keypoints_2d[18*3]
oidoIzq_y=perfil_pose_keypoints_2d[18*3+1]
bigToeIzq_x=perfil_pose_keypoints_2d[19*3]
bigToeIzq_y=perfil_pose_keypoints_2d[19*3+1]
smallToeIzq_x=perfil_pose_keypoints_2d[20*3]
smallToeIzq_y=perfil_pose_keypoints_2d[20*3+1]
talonIzq_x=perfil_pose_keypoints_2d[21*3]
talonIzq_y=perfil_pose_keypoints_2d[21*3+1]
bigToeDer_x=perfil_pose_keypoints_2d[22*3]
bigToeDer_y=perfil_pose_keypoints_2d[22*3+1]
smallToeDer_x=perfil_pose_keypoints_2d[23*3]
smallToeDer_y=perfil_pose_keypoints_2d[23*3+1]
talonDer_x=perfil_pose_keypoints_2d[24*3]
talonDer_y=perfil_pose_keypoints_2d[24*3+1]
#background_x=perfil_pose_keypoints_2d[25*3]
#background_y=perfil_pose_keypoints_2d[25*3+1]


print(hombroDer_y)
print(hombroIzq_y)
print(caderaDer_y)
print(caderaIzq_y)
print(rodillaDer_y)
print(rodillaIzq_y)
print(talonDer_y)
print(talonIzq_y)
print("relacion entre cadera/talon eje x derecho: ")
print(abs(caderaDer_x-talonDer_x))
print("relacion entre cadera/talon eje x ixquierdo: ")
print(abs(caderaIzq_x-talonIzq_x))

print(" PARA AGARRE CERRADO: relacion entre mano/rodilla eje x ixquierdo: ") # para agarre cerrado deberia ser menos de 100
print(abs(muñecaIzq_x-rodillaIzq_x))
print(" PARA AGARRE CERRADO: relacion entre mano/rodilla eje x derecho: ")
print(abs(muñecaDer_x-rodillaDer_x))





print("PARA EXENSIÓN COMPLETA DE CADERA: ")
print("Esto habría que mirarlo en un vídeo grabadod de perfil")
print("Al final del movimiento debe ocurrir que cadera, rodillas, hombros estén alineados, es decir que la diferencia entre el eje x sea casi nulo")
#si los hombros se queddan por delante -> echa los hombros hacia atras
# si los la rodilla se queda flexionada-> estira la rodilla
#relamente esto sería con lso datos del perfil:
# y realmente desde un unico lado se de debería saber, el lado q está mas cerca de la cámara
print(abs(caderaDer_x-hombroDer_x))
print(abs(caderaDer_x-rodillaDer_x))
print(abs(caderaIzq_x-hombroIzq_x))
print(abs(caderaIzq_x-rodillaIzq_x))





print("PARA EXENSIÓN COMPLETA DE CODOS: ")
print("Esto habría que mirarlo en un vídeo grabadod de perfil")
print("Al final del movimiento debe ocurrir que cadera, rodillas, hombros estén alineados, es decir que la diferencia entre el eje x sea casi nulo")
#si los hombros se queddan por delante -> echa los hombros hacia atras
# si los la rodilla se queda flexionada-> estira la rodilla
#relamente esto sería con lso datos del perfil:
# y realmente desde un unico lado se de debería saber, el lado q está mas cerca de la cámara
print(abs(caderaDer_x-hombroDer_x))
print(abs(caderaDer_x-rodillaDer_x))
print(abs(caderaIzq_x-hombroIzq_x))
print(abs(caderaIzq_x-rodillaIzq_x))


##frontal agarre de snatch
## perfil agarre declean






print(" PARA AGARRE CERRADO: relacion entre mano/rodilla eje x ixquierdo: ") # para agarre cerrado deberia ser menos de 100
print(abs(muñecaIzq_x-rodillaIzq_x))
print(abs(muñecaDer_x-rodillaDer_x))

print(" PARA BARRA PEGADAAL CUERPO : relacion entre mano y talon ") # para agarre cerrado deberia ser menos de 100
print(abs(muñecaIzq_x-talonIzq_x))
print(abs(muñecaDer_x-talonDer_x)) # este lado no se me ve bien


print("para peso bien distribuido, relacion rodilla-punta pie")
print("Si en algun momento es negativo quiere decir q la rodilla adelanta al pie")
print(smallToeIzq_x-rodillaIzq_x)


print("PARA EXTENSION DE CADERAS Y RODILLAS")
print("analizamos hombros, caderas y rodillas")
print(abs(tobilloIzq_x-hombroIzq_x))
print(abs(tobilloIzq_x-hombroIzq_x))



print("Mantener la espalda recta")
print("Analizamos diferencia entre hombros y cadera enel eje y")
print("Si en las primeras posiciones  la diferencia enel eje y entre hombro y cadera es muy pequeña, está doblando la espalda")
print(abs(caderaIzq_y-hombroIzq_y))




print(" PARA AGARRE CERRADO: relacion entre mano/rodilla eje x ixquierdo: ") # para agarre cerrado deberia ser menos de 100
print(abs(muñecaIzq_x-rodillaIzq_x))
print(" PARA AGARRE CERRADO: relacion entre mano/rodilla eje x derecho: ")
print(abs(muñecaDer_x-rodillaDer_x))


print("rodiollas")
print(rodillaIzq_x)
print(rodillaIzq_y)
print(rodillaDer_x)
print(rodillaDer_y)

print("")
print("caderas")
print(caderaIzq_x)
print(caderaIzq_y)
print(caderaDer_x)
print(caderaDer_y)
print(caderaCentral_x)
print(caderaCentral_y)


print("hombros")
print(hombroIzq_x)
print(hombroIzq_y)
print(hombroDer_x)
print(hombroDer_y)


print("")
print("big toes")
print(bigToeIzq_x)
print(bigToeIzq_y)
print("small toes")
print(smallToeIzq_x)
print(smallToeIzq_y)
print("talones")
print(talonDer_x)
print(talonDer_y)





print("para peso bien distribuido en pies, no me voy a las puntillas")
print(abs(smallToeIzq_y-talonIzq_y))
print("big toe con talon")
print(bigToeIzq_y-talonIzq_y)




print("RODILLAS POR DELANTE DE PIE(esto tambien podría sevirme para peso bien distribuido de pies)")
print(rodillaIzq_x-bigToeIzq_x) # si la adelanta tiene que se negativo
print("big toe con talon")
print(talonIzq_y-bigToeIzq_y) # si se levanta el talon, va a salir negativo tambien

#print(rodillaIzq_x-smallToeIzq_x)



print("PARA EXTENSION DE CADERAS Y RODILLAS")
print("analizamos hombros, caderas y rodillas") # debemos comprobarlo al principio y al final del video no ?
print(abs(tobilloIzq_x-rodillaIzq_x))
print(abs(caderaIzq_x-hombroIzq_x))

#estos no creo que me sirvan
print(abs(tobilloIzq_x-caderaIzq_x))
print(abs(tobilloIzq_x-hombroIzq_x))
print(abs(rodillaIzq_x-caderaIzq_x))
print(abs(rodillaIzq_x-hombroIzq_x))


print("Para VERTICALIDAD DE BARRA EN EMPUJES")
print("Analizamos mueñeca-tobillo ")
print(abs(muñecaIzq_x-tobilloIzq_x))
print("Tambien podemos analizar muñeca- codo . que la muñeca no adelante al codoen ningun momento")
print(muñecaIzq_x-codoIzq_x)



print("PARA BARRA APOYADA EN HOMBROS EN FRONT RACK")
print("que hombros y muñecas estén muyy cerca")
print(muñecaDer_y - hombroDer_y)
print(muñecaIzq_y - hombroIzq_y)
# no debe ser mayor q un numero positivo



print("CODOS POSICIÓN DE FRONT RACK")
print("Que los  codos estén mas o menos  a la altura de los hombros ")
print(codoIzq_y - hombroIzq_y) #  coefienciento <= numero (numero positivo cercano al 0)

print("ROMPER EL PARALELO")
print("Que la cadera quede por debajo de las rodillas")
print(caderaIzq_y-rodillaIzq_y) 
# si esto es negativo, no está rompiendo el paralelo
#entonces buscaremos que se cumpla x veces para decir que se rompe


print("EXTENSION DE CODOS ")
print("Dado dos puntos (muñeca hombro) tengo una recta y entonces el punto del cododebe estar en esa recta")
#lado derecho
#y = mx + n
m = (muñecaDer_y - hombroDer_y) / (muñecaDer_x - hombroDer_x)
n = hombroDer_y - (m * hombroDer_x)



print(codoDer_y)
print(m * codoDer_x + n)





m = (muñecaIzq_y - hombroIzq_y) / (muñecaIzq_x - hombroIzq_x)
n = muñecaIzq_y - m * muñecaIzq_x
print(codoIzq_y)
print(m * codoIzq_x + n)


     
print("RODILLAS SIGUEN LA LINEA DEL PIE")
print("Para cada rodilla es diferente")
print("rodilla DERECHA ")
print(rodillaDer_x - bigToeDer_x) #si esto es mucho mayor que 0, quiere decir que está metiendo las rodillas
print("rodilla izquierda")
print(rodillaIzq_x- bigToeIzq_x) # si esto es negativo, quiere decir que está metiendola rodilla



print("ANCHURA PIES CADERA")
print(tobilloIzq_x - caderaIzq_x) # deben ser cercano a 0
print(tobilloDer_x -caderaDer_x)

print("ANCHURA PIES HOMBROS")
print(tobilloIzq_x - hombroIzq_x) # deben ser cercano a 0
print(tobilloDer_x -hombroDer_x)








print("PARA BARRA APOYADA EN HOMBROS EN FRONT RACK")
print("que hombros y muñecas estén muyy cerca")
print(muñecaDer_y - hombroDer_y)
print(muñecaIzq_y - hombroIzq_y)
# no debe ser mayor q un numero positivo
