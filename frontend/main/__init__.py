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

    #Importar Blueprints
    from main.routes import main, user, poem, my
    app.register_blueprint(main.main)
    app.register_blueprint(user.user)
    app.register_blueprint(poem.poem)
    app.register_blueprint(my.my)

    #Retornar aplicación inicializada
    return app
