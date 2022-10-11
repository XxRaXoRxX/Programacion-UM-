from flask import Blueprint, redirect, url_for, render_template, request
import requests
import json

#Crear Blueprint
my = Blueprint('my', __name__, url_prefix='/my')

# Ver información del usuario
@my.route('/')
def index():
    return render_template('user_info.html')

# Ver poemas del usuario
@my.route('/poems')
def poems():
    
    # TODO: URL hardcodeada. Madar esto a __init__.py
    api_url = "http://127.0.0.1:8500/poems"

    # Envio de la pagina y cuantos datos por pagina.
    data = {"page": 1, "perpage": 3}

    # Obtengo el jwt del logueo e instancio headers y le agrego el jwt.
    jwt = request.cookies.get("access_token")
    headers = {"Content-Type" : "application/json", "Authorization" : f"BEARER {jwt}"}

    # Creamos el response y le enviamos el data y headers.
    resp = requests.get(api_url, json = data, headers = headers)

    # Guardamos los poemas en una variable.
    poems = json.loads(resp.text)
    poemsList = poems["poems"]

    return render_template('user_poems.html', poems = poemsList)

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

