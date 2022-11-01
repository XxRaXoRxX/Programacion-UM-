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

    if (jwt):
        user = auth.load_user(jwt)
        
        # Guardamos la información de usuario en una variable.
        user_info = func.get_user_info(user["id"])
        user_info = json.loads(user_info.text)

        return render_template('user_info.html', jwt = jwt, user_info = user_info)
    else:
        return redirect(url_for('main.login'))

# Ver poemas del usuario
@my.route('/poems')
def poems():

    jwt = func.get_jwt()
    if (jwt):
        user = auth.load_user(jwt)
        resp = func.get_poems_by_id(user["id"])

        # Guardamos los poemas en una variable.
        poems = json.loads(resp.text)
        poemsList = poems["poems"]

        return render_template('user_poems.html', jwt = jwt, poems = poemsList)
    else:
        return redirect(url_for('main.login'))

# Editar usuario
@my.route('/edit', methods=['GET', 'POST'])
def edit():
    if(request.method == "POST"):
        # Obtener el nuevo nickname y cambiar nombre de usuario.
        nick = request.form.get("editar_nick")
        func
    else:
        jwt = func.get_jwt()
        if (jwt):
            user = auth.load_user(jwt)

            # Guardamos la información de usuario en una variable.
            user_info = func.get_user_info(user["id"])
            user_info = json.loads(user_info.text)

            return render_template('user_config.html', jwt = jwt, user = user_info)
        else:
            return redirect(url_for('main.login'))

# Eliminar cuenta del usuario
@my.route('/delete')
def delete():
    return render_template('delete_account.html')

# Cambiar contraseña del usuario
@my.route('/password')
def password():
    return render_template('change_password.html')

