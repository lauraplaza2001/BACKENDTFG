import subprocess

comando1 = "py -m uvicorn usuario:api --reload --port 8000 --host 0.0.0.0"
comando2 = "py -m uvicorn ejercicio:api --reload --port 8001 --host 0.0.0.0"
comando3 = "py -m uvicorn informe:api --reload --port 8002 --host 0.0.0.0"


proceso1 = subprocess.Popen(comando1, shell=True)
proceso2 = subprocess.Popen(comando2, shell=True)
proceso3 = subprocess.Popen(comando3, shell=True)


proceso1.wait()
proceso2.wait()
proceso3.wait()

print("Todos los comandos han terminado.")
