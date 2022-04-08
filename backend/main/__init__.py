import os
import resource
from flask import Flask
from dotenv import load_dotenv
from flask_restful import Api
import main.resources as resource

api = Api()

def create_app():
    #inicializar Flask
    app= Flask(__name__)
    #Cargar variables de entorno
    load_dotenv()
    api.add_resource(resource.PoemsResource, '/poems')
    api.add_resource(resource.PoemResource, '/poem/<id>')
    api.add_resource(resource.UsersResource, '/users')
    api.add_resource(resource.UserResource, '/user/<id>')
    api.add_resource(resource.MarksResource, '/marks')
    api.add_resource(resource.MarkResource, '/mark/<id>')
    #Aqui se inicializaran el resto de los m
    #retornar aplicaciion inicializada
    api.init_app(app)
    return app

