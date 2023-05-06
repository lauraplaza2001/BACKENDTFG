import requests

url = 'https://res.cloudinary.com/drcsegsao/video/upload/v1679735658/TFG/esteeselnombre.mp4'
response = requests.get(url)

with open('videos/perfil.mp4', 'wb') as f:
    f.write(response.content)
