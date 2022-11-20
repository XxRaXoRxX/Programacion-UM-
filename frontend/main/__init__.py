import os
from flask import Flask
from dotenv import load_dotenv
from flask_login import LoginManager, login_required

login_manager = LoginManager()

# Metodo que inicializara todos los modulos y variables
def create_app():
    # Inicializar Frask
    app = Flask (__name__)

    # Cargar variables de entorno
    load_dotenv()

    # Cargar API_URL del backend, Siendo la dirección del backend.
    app.config["API_URL"] = os.getenv("API_URL")

    #Cargar clave secreta de JWT
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

    # Utilizado para el auth.py de la carpeta routes, para el manejo de jwt.
    login_manager.init_app(app)

    #Iniciar el resto de las extensiones.
    #Extensiones

    #Importar Blueprints, siendo las rutas del html.
    from main.routes import main, user, poem, my
    app.register_blueprint(main.main)
    app.register_blueprint(user.user)
    app.register_blueprint(poem.poem)
    app.register_blueprint(my.my)

    #Retornar aplicación inicializada
    return app
