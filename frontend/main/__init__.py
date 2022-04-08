import os
from flask import Flask
from dotenv import load_dotenv

# Metodo que inicializara todos los modulos y variables
def create_app():
    #Inicializar Frask
    app = Flask (__name__)

    #Cargar variables de entorno
    load_dotenv()

    #Iniciar el resto de las extensiones.
    #Extensiones

    #Retornar aplicación inicializada
    return app
