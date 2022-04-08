import os
import sys
import resource
from flask import Flask
from dotenv import find_dotenv, load_dotenv
from flask_restful import Api
import main.resources as resource

api = Api()

# Metodo que inicializara todos los modulos y variables
def create_app():
<<<<<<< HEAD
    
    #inicializar Flask
    app = Flask(__name__)
    
=======
    #Inicializar Flask
    app= Flask(__name__)

>>>>>>> cf616dc640792817b620a3cee17a9b87b45fa97d
    #Cargar variables de entorno
    path = sys.path[0]
    load_dotenv(path) 		#TODO: Por alguna razón esto no esta funcionando y no me trae el PORT dentro del .env. Consultar con profe
    api.add_resource(resource.PoemsResource, '/poems')
    api.add_resource(resource.PoemResource, '/poem/<id>')
    api.add_resource(resource.UsersResource, '/users')
    api.add_resource(resource.UserResource, '/user/<id>')
    api.add_resource(resource.MarksResource, '/marks')
    api.add_resource(resource.MarkResource, '/mark/<id>')
    
    #Iniciar el resto de las extensiones.
<<<<<<< HEAD
    #Extensiones
    api.init_app(app)
    
=======
    api.init_app(app)

>>>>>>> cf616dc640792817b620a3cee17a9b87b45fa97d
    #Retornar aplicación inicializada
    return app

