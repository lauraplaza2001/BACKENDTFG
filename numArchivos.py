import os

dir_path = 'InfoOpenPose/json/frontalJson'
files = os.listdir(dir_path)
print(files)

print("Número de archivos en la carpeta:", len(files))
