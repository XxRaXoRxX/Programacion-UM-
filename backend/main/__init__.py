import os
import sys
import resource
from flask import Flask
from dotenv import load_dotenv
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

#Inicializar flask
api = Api()

#inicializar la base de datos
db = SQLAlchemy()

def create_app():
    
    #inicializar Flask
    app = Flask(__name__)

    #cargamos variables de archivo .env
    load_dotenv()

    # Data Base
    #Si no existe el archivo de base de datos crearlo (solo válido si se utiliza SQLite)
    print(os.getenv('DATABASE_PATH'))
    if not os.path.exists(os.getenv('DATABASE_PATH')+os.getenv('DATABASE_NAME')):
        os.mknod(os.getenv('DATABASE_PATH')+os.getenv('DATABASE_NAME'))

    # Esto es para evitar que la base de datos trackee los cambios
    #app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Url de configuración de base de datos. Solo funcional para SQLite.
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////'+os.getenv('DATABASE_PATH')+os.getenv('DATABASE_NAME')

    # Iniciamos la base de datos.
    db.init_app(app)
    # Data Base

    #Importamos main.resources luego de crear la base de datos.
    import main.resources as resource
    
    #Cargar variables de entorno
    api.add_resource(resource.PoemsResource, '/poems')
    api.add_resource(resource.PoemResource, '/poem/<id>')
    api.add_resource(resource.UsersResource, '/users')
    api.add_resource(resource.UserResource, '/user/<id>')
    api.add_resource(resource.MarksResource, '/marks')
    api.add_resource(resource.MarkResource, '/mark/<id>')
    
    #Iniciar el resto de las extensiones.
    #Extensiones
    api.init_app(app)
    
    #Retornar aplicación inicializada
    return app

