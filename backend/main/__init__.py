import os
import sys
import resource
from flask import Flask
from dotenv import load_dotenv
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_mail import Mail

#Inicializar flask
api = Api()

#inicializar la base de datos
db = SQLAlchemy()

#Inicializar el generador de Tokens.
jwt = JWTManager()

#Inicializar el envio de mails.
mailsender = Mail()

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

    #Cargar clave secreta de JWT
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    #Cargar tiempo de expiración de los tokens de JWT
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES'))
    #Iniciar el JWT
    jwt.init_app(app)

    #Importamos main.resources luego de crear la base de datos.
    from main.auth import routes
    #Importar Blueprint
    app.register_blueprint(routes.auth)
    
    #Configuración de mail
    app.config['MAIL_HOSTNAME'] = os.getenv('MAIL_HOSTNAME')
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
    app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS')
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['FLASKY_MAIL_SENDER'] = os.getenv('FLASKY_MAIL_SENDER')
    #Inicializar el mail en app
    mailsender.init_app(app)
    
    #Retornar aplicación inicializada
    return app

