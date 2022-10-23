from flask import Blueprint, current_app, redirect, url_for, render_template, request
from . import functions as func
from . import auth as auth
import requests
import json

#Crear Blueprint
my = Blueprint('my', __name__, url_prefix='/my')

# Ver información del usuario
@my.route('/')
def index():
    # traemos el token de las cookies.
    jwt = func.get_jwt()
    print(jwt)
    user = auth.load_user(jwt)
    
    # TODO: URL hardcodeada. Madar esto a __init__.py
    api_url = f'{current_app.config["API_URL"]}/user/{user["id"]}'

    # Guardamos la información de usuario en una variable.
    user_info = func.get_user_info(api_url)
    user_info = json.loads(user_info.text)

    return render_template('user_info.html', jwt = jwt, user_info = user_info)

# Ver poemas del usuario
@my.route('/poems')
def poems():
    # TODO: URL hardcodeada. Madar esto a __init__.py
    api_url = f'{current_app.config["API_URL"]}/poems'

    jwt = func.get_jwt()
    #id = func.get_id()
    resp = func.get_poems_by_id(api_url, id)

    # Guardamos los poemas en una variable.
    poems = json.loads(resp.text)
    poemsList = poems["poems"]

    return render_template('user_poems.html', jwt = jwt, poems = poemsList)

# Editar usuario
@my.route('/edit')
def edit():
    return render_template('user_config.html')

# Eliminar cuenta del usuario
@my.route('/delete')
def delete():
    return render_template('delete_account.html')

# Cambiar contraseña del usuario
@my.route('/password')
def password():
    return render_template('change_password.html')

