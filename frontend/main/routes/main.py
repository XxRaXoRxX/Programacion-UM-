from flask import Blueprint, redirect, current_app, url_for, render_template, make_response, request
from . import functions as func
import requests
import json

#Crear Blueprint
main = Blueprint('main', __name__, url_prefix='/')

# Ruta menu principal con poemas
@main.route('/')
def index():
    api_url = f'{current_app.config["API_URL"]}/poems'

    jwt = func.get_jwt()
    resp = func.get_poems(api_url)

    # Guardamos los poemas en una variable.
    poems = json.loads(resp.text)
    poemsList = poems["poems"]

    return render_template('main.html', jwt = jwt, poems = poemsList)

# Ruta menu principal con poemas
@main.route('/login', methods=['GET', 'POST'])
def login():
    if(request.method == "POST"):
        # Obtener password y email
        email = request.form.get("email")
        password = request.form.get("contraseña")

        if email != None and password != None:
            api_url = f'{current_app.config["API_URL"]}/auth/login'

            # Envio de logueo.
            data = {"email": email, "password": password}
            headers = {"Content-Type" : "application/json"}

            # Generamos la respuesta, mandando endpoint, data diccionario, y el headers que es el formato como aplication json.
            response = requests.post(api_url, json = data, headers = headers)
            
            if (response.ok):
                # Obtener el token desde response.
                response = json.loads(response.text)
                token = response["access_token"]
                user_id = str(response["id"])

                api_url = f'{current_app.config["API_URL"]}/poems'
                resp = func.get_poems(api_url)

                # Guardamos los poemas en una variable.
                poems = json.loads(resp.text)
                poemsList = poems["poems"]

                # Guardar el token en las cookies y devuelve la página.
                resp = make_response(render_template("main.html", jwt = token, poems = poemsList))
                resp.set_cookie("access_token", token)
                return resp

        # TODO: Mostrar mensaje de error de logueo.
        return render_template("login.html")
    else:
        return render_template("login.html")