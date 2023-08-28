import requests
import time 

max_retries = 3  # Número máximo de intentos
retry_delay = 5  # Tiempo de espera entre reintentos en segundos
url = "https://ecb4-34-147-30-186.ngrok-free.app/openPose"
print("hola")

for retry in range(max_retries):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Lanzará una excepción si el código de estado no es exitoso (>= 400)
        print("Solicitud realizada correctamente")
        break  # Salir del bucle si la solicitud es exitosa
    except requests.exceptions.RequestException as e:
        print(f"Error al realizar la solicitud en el intento {retry + 1}: {e}")
        if retry < max_retries - 1:
            print(f"Reintentando en {retry_delay} segundos...")
            time.sleep(retry_delay)
        else:
            print("Se ha alcanzado el número máximo de intentos.")
