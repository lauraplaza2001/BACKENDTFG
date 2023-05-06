import os

carpeta = 'videos'
for archivo in os.listdir(carpeta):
    archivo_path = os.path.join(carpeta, archivo)
    if os.path.isfile(archivo_path) or os.path.islink(archivo_path):    
         os.unlink(archivo_path)
    elif os.path.isdir(archivo_path):
        os.rmdir(archivo_path)
    

carpeta = 'InfoOpenPose/json/frontalJson'
for archivo in os.listdir(carpeta):
    archivo_path = os.path.join(carpeta, archivo)
    if os.path.isfile(archivo_path) or os.path.islink(archivo_path):
        os.unlink(archivo_path)
    elif os.path.isdir(archivo_path):
        os.rmdir(archivo_path)


carpeta = 'InfoOpenPose/json/perfilJson'
for archivo in os.listdir(carpeta):
    archivo_path = os.path.join(carpeta, archivo)
    if os.path.isfile(archivo_path) or os.path.islink(archivo_path):
        os.unlink(archivo_path)
    elif os.path.isdir(archivo_path):
        os.rmdir(archivo_path)

