from flask import Blueprint, redirect, url_for, render_template, make_response, request
import requests
import json

def get_poems_by_id(api_url, id, page = 1, perpage = 3):
    # Envio de la pagina y cuantos datos por pagina.
    data = {"page": page, "perpage": perpage, "userID": id}

    # Obtengo el jwt del logueo e instancio headers y le agrego el jwt.
    headers = get_headers(without_token = True)

    # Creamos el response y le enviamos el data y headers.
    return requests.get(api_url, json = data, headers = headers)

def get_poems(api_url, page = 1, perpage = 3):
    # Envio de la pagina y cuantos datos por pagina.
    data = {"page": page, "perpage": perpage}

    # Obtengo el jwt del logueo e instancio headers y le agrego el jwt.
    headers = get_headers()

    # Creamos el response y le enviamos el data y headers.
    return requests.get(api_url, json = data, headers = headers)

def get_user_info(api_url):
    # Obtengo el jwt del logueo e instancio headers y le agrego el jwt.
    headers = get_headers()

    # Creamos el response y le enviamos el data y headers.
    return requests.get(api_url, headers = headers)

def get_headers(without_token = False):
    jwt = get_jwt()
    if jwt and without_token == False:
        return {"Content-Type" : "application/json", "Authorization" : f"Bearer {get_jwt()}"}
    else:
        return {"Content-Type" : "application/json"}

def get_jwt():
    return request.cookies.get("access_token")

def get_username(user_id):
    # Obtengo el jwt del logueo e instancio headers y le agrego el jwt.
    headers = get_headers()
    api_url = f"http://127.0.0.1:8500/user/{user_id}"

    resp = requests.get(api_url, headers = headers)
    user = json.loads(resp.text)
    return user["name"]
