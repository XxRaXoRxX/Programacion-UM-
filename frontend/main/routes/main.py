from flask import Blueprint, redirect, url_for, render_template, make_response
import requests
import json

#Crear Blueprint
main = Blueprint('main', __name__, url_prefix='/')

# Ruta menu principal con poemas
@main.route('/')
def index():
    return render_template('main.html')

# Ruta menu principal con poemas
@main.route('/login')
def login():
    # TODO: URL hardcodeada. Mandar esto a __init__.py
    api_url = "http://127.0.0.1:8500/auth/login"

    # Envio de logueo.
    data = {"email": "usuario@usuario.com", "password": "123"}
    headers = {"Content-Type" : "application/json"}
    response = requests.post(api_url, json = data, headers = headers)

    # Obtener el token desde response.
    token = json.loads(response.text)
    token = token["access_token"]

    # Guardar el token en las cookies y devuelve la página.
    resp = make_response(render_template("login.html"))
    resp.set_cookie("access_token", token)
    return resp

    #return render_template('login.html')