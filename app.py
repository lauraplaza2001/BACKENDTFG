from flask import Flask
from flask_ngrok import run_with_ngrok
from IPython.display import IFrame

app = Flask(__name__)
run_with_ngrok(app)




@app.route("/")
def home():
   return "hola"

if __name__ == "__main__":
    app.run()
