from tokenize import Token
from flask import Blueprint, redirect, current_app, url_for, render_template, make_response, request
from . import functions as func
import requests
import json

#Crear Blueprint
main = Blueprint('main', __name__, url_prefix='/')

# Ruta menu principal con poemas
@main.route('/')
def index(jwt = None):
    if (jwt == None):
        jwt = func.get_jwt()

    resp = func.get_poems(jwt = jwt)

    # Guardamos los poemas en una variable.
    poems = func.get_json(resp)
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
            response = func.login(email, password)
            
            if (response.ok):
                # Obtener el token desde response.
                response = json.loads(response.text)
                token = response["access_token"]

                # Guardar el token en las cookies y devuelve la página.
                resp = make_response(index(jwt=token))
                resp.set_cookie("access_token", token)
                return resp

        # TODO: Mostrar mensaje de error de logueo.
        return render_template("login.html")
    else:
        return render_template("login.html")