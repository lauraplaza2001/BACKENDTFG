from flask_ngrok import run_with_ngrok
from flask import Flask, render_template , request 
import os
from google.colab import drive
drive.mount('/content/gdrive')
PEOPLE_FOLDER = os.path.join('static', 'people_photo')
app = Flask(__name__, template_folder='/content/static')
app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER
run_with_ngrok(app)
@app.route('/')
def home():
  full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'Shovon.jpg')
  return render_template('Webp.html',user_image = full_filename)
if __name__ == '__main__':
   app.run()