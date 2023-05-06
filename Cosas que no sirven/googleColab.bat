conda activate nombre_del_entorno
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client jupyter_http_over_ws
jupyter serverextension enable --py jupyter_http_over_ws
jupyter notebook --NotebookApp.allow_origin='https://colab.research.google.com' --port=8888 --NotebookApp.port_retries=0




conda create --name myenv python=3.10.9
conda activate myenv

en bash : 
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
pip install papermill





pip install google-colab
