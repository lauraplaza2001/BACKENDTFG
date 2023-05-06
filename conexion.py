from google.colab import auth
from google.colab import drive
import requests



auth.authenticate_user()




# Pegue aquí el enlace que ha copiado de Google Colab
notebook_link = "https://colab.research.google.com/drive/1S-rTdybbq19CLphy2ONl9AJSub1hDuxT?usp=sharing"

# Carga el contenido del cuaderno de Google Colab
response = requests.get(notebook_link)
notebook_content = response.text

# Ejecuta el cuaderno de Google Colab con los parámetros especificados
parameters = {"param1": "value1", "param2": "value2"}
exec(notebook_content, parameters)
