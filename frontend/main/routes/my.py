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

    jwt = func.get_jwt()

    if(request.method == "POST"):
        if (jwt):
            # Obtener el nuevo nickname
            nick = request.form.get("editar_nick")
            
            user = auth.load_user(jwt)

            if nick != "":
                # Cambiar nombre de usuario en la base de datos.
                resp = func.put_username(user["id"], nick)

                # Guardamos la información de usuario en una variable.
                user_info = func.get_user_info(user["id"])
                user_info = json.loads(user_info.text)

                if (resp.ok):
                    return render_template('user_config.html', jwt = jwt, user = user_info, success = "Nombre de usuario cambiado correctamente")
                else:
                    return render_template('user_config.html', jwt = jwt, user = user_info, error = "No se ha podido cambiar el nombre de usuario")
            else:
                # Guardamos la información de usuario en una variable.
                user_info = func.get_user_info(user["id"])
                user_info = json.loads(user_info.text)

                return render_template('user_config.html', jwt = jwt, user = user_info, error = "El nombre de usuario no puede estar vacío")       
    else:   
        if (jwt):
            user = auth.load_user(jwt)

            # Guardamos la información de usuario en una variable.
            user_info = func.get_user_info(user["id"])
            user_info = json.loads(user_info.text)

            return render_template('user_config.html', jwt = jwt, user = user_info)
    
    return redirect(url_for('main.login'))

# Eliminar cuenta del usuario
@my.route('/delete')
def delete():
    return render_template('delete_account.html')

# Cambiar contraseña del usuario
@my.route('/password', methods=['GET', 'POST'])
def password():
    jwt = func.get_jwt()

    if(request.method == "POST"):
        if (jwt):
            # Obtener la nueva contraseña
            actual_pass = request.form.get("actual_password")
            new_pass = request.form.get("new_password")
            
            # Obtener datos del usuario
            user = auth.load_user(jwt)
            email = user["email"]

            print(email, actual_pass)

            if email != "" and actual_pass != "":
                response = func.login(email, actual_pass)
            
                if (response.ok):
                    # Cambiar contraseña en la base de datos.
                    resp = func.put_password(user["id"], new_pass)

                    if (resp.ok):
                        return render_template('change_password.html', jwt = jwt, success = "Contraseña cambiada correctamente")
                
            return render_template('change_password.html', jwt = jwt, error = "No se ha podido cambiar la contraseña")
    else:
        if (jwt):
            return render_template('change_password.html', jwt = jwt)
    
    return redirect(url_for('main.login'))