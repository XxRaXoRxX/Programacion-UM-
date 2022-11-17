from tokenize import Token
from flask import Blueprint, redirect, current_app, url_for, render_template, make_response, request
from . import functions as func
import requests
import json

#Crear Blueprint
main = Blueprint('main', __name__, url_prefix='/')

# Ruta menu principal con poemas
@main.route('/', methods=['GET', 'POST'])
def index(jwt = None):

    if (jwt == None):
        jwt = func.get_jwt()

    if(request.method == "POST"):
        filter_title = request.form.get("filter_title")
        filter_author = request.form.get("filter_author")
        filter_rating = request.form.get("filter_rating")

        # Obtener los poemas.
        resp = func.get_poems_by_fiters(title= filter_title, author= filter_author, rating= filter_rating)

        # Guardamos los poemas en una variable.
        poems = func.get_json(resp)
        poemsList = poems["poems"]

        return render_template('main.html', jwt = jwt, poems = poemsList)
    else:
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

        if email != "" and password != "":
            response = func.login(email, password)
            
            if (response.ok):
                # Obtener el token desde response.
                response = json.loads(response.text)
                token = response["access_token"]

                # Guardar el token en las cookies y devuelve la página.
                resp = make_response(redirect(url_for('main.index')))
                #resp = make_response(redirect(url_for('main.index'), token))
                resp.set_cookie("access_token", token)
                return resp

        # TODO: Mostrar mensaje de error de logueo.
        return render_template("login.html", error = "Usuario y contraseña incorrectos")
    else:
        return render_template("login.html")

# Ruta menu principal con poemas
@main.route('/register', methods=['GET', 'POST'])
def register():
    if(request.method == "POST"):
        # Obtener password y email
        email = request.form.get("email")
        password = request.form.get("contraseña")
        name = request.form.get("nombre")

        if email != "" and password != "" and name != "":
            response = func.register(name, email, password)
            
            if (response.ok):
                # Lo manda a la pagina del login.
                resp = render_template("login.html", success = "Usuario registrado correctamente")
                return resp

        # TODO: Mostrar mensaje de error de logueo.
        return render_template("register.html", error = "Datos ingresados incorrectos")
    else:
        return render_template("register.html")

@main.route('/logout')
def logout():
    resp = make_response(redirect('login'))
    resp.set_cookie('access_token', '', expires=0)
    return resp