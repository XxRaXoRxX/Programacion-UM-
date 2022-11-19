from flask import Blueprint, redirect, url_for, render_template, make_response, request, current_app
import requests
import json
from . import auth

# -- Poems --
def get_poems_by_id(id, title = "", rating = None, page = 1, perpage = 3):
    api_url = f'{current_app.config["API_URL"]}/poems'
    # Envio de la pagina y cuantos datos por pagina.
    if (rating == None):
        data = {"page": page, "perpage": perpage, "title": title, "userID": id}
    else:
        data = {"page": page, "perpage": perpage, "userID": id, "title": title, "rating": int(rating)}

    # Obtengo el jwt del logueo e instancio headers y le agrego el jwt.
    headers = get_headers(without_token = True)

    # Creamos el response y le enviamos el data y headers.
    return requests.get(api_url, json = data, headers = headers)

def get_poems(jwt = None, page = 1, perpage = 3):
    api_url = f'{current_app.config["API_URL"]}/poems'
    # Envio de la pagina y cuantos datos por pagina.
    data = {"page": page, "perpage": perpage}

    # Obtengo el jwt del logueo e instancio headers y le agrego el jwt.
    if (jwt):
        headers = get_headers(jwt = jwt)
    else:
        headers = get_headers(without_token = True)

    # Creamos el response y le enviamos el data y headers.
    return requests.get(api_url, json = data, headers = headers)

def get_poems_by_fiters(title = "", author = "", rating = None, page = 1, perpage = 3):
    api_url = f'{current_app.config["API_URL"]}/poems'
    # Envio de la pagina y cuantos datos por pagina.

    if (title == None):
        title = ""
    if (author == None):
        author = ""
    
    if (rating == None):
        data = {"page": page, "perpage": perpage, "title": title, "username": author}
    else:
        data = {"page": page, "perpage": perpage, "title": title, "username": author, "rating": int(rating)}

    # Para obtener filtros, solo se puede en usuarios sin token.
    headers = get_headers(without_token = True)

    # Creamos el response y le enviamos el data y headers.
    return requests.get(api_url, json = data, headers = headers)

def get_poems_page():
    return request.cookies.get("poems_page")
# -- Poems --

# -- Poem --
def create_poem(id, titulo_poema, cuerpo_poema):
    api_url = f'{current_app.config["API_URL"]}/poems'
    data = {"title":titulo_poema, "userID":id, "body":cuerpo_poema}
    headers = get_headers()

    return requests.post(api_url, json = data, headers = headers)

def edit_poem(id, titulo_poema, cuerpo_poema):
    api_url = f'{current_app.config["API_URL"]}/poem/{id}'
    data = {"title":titulo_poema, "body":cuerpo_poema}
    headers = get_headers()

    return requests.put(api_url, json = data, headers = headers)

def get_poem(id, jwt = None):
    api_url = f'{current_app.config["API_URL"]}/poem/{id}'
    
    # Obtengo el jwt del logueo e instancio headers y le agrego el jwt.
    if (jwt):
        headers = get_headers(jwt = jwt)
    else:
        headers = get_headers(without_token = True)

    return requests.get(api_url, headers = headers)

def delete_poem(poem_id, jwt = None):
    api_url = f'{current_app.config["API_URL"]}/poem/{poem_id}'
    
    # Obtengo el jwt del logueo e instancio headers y le agrego el jwt.
    if (jwt):
        headers = get_headers(jwt = jwt)
    else:
        headers = get_headers(without_token = True)

    return requests.delete(api_url, headers = headers)
# -- Poem --

# -- User --
def get_user_info(user_id):
    api_url = f'{current_app.config["API_URL"]}/user/{user_id}'
    # Obtengo el jwt del logueo e instancio headers y le agrego el jwt.
    headers = get_headers()

    # Creamos el response y le enviamos el data y headers.
    return requests.get(api_url, headers = headers)

def get_username(user_id):
    api_url = f'{current_app.config["API_URL"]}/user/{user_id}'
    # Obtengo el jwt del logueo e instancio headers y le agrego el jwt.
    headers = get_headers()

    resp = requests.get(api_url, headers = headers)
    user = get_json(resp)
    return user["name"]

def put_username(user_id, name):
    api_url = f'{current_app.config["API_URL"]}/user/{user_id}'
    data = {"id": user_id, "name": name}
    headers = get_headers()

    return requests.put(api_url, json = data, headers = headers)

def put_password(user_id, password):
    api_url = f'{current_app.config["API_URL"]}/user/{user_id}'
    data = {"id": user_id, "password": password}
    headers = get_headers()

    return requests.put(api_url, json = data, headers = headers)
# -- User --

# -- Marks --
def get_marks(poem_id, jwt = None):
    api_url = f'{current_app.config["API_URL"]}/marks'

    data = {"poem_id": poem_id}
    
    # Obtengo el jwt del logueo e instancio headers y le agrego el jwt.
    if (jwt):
        headers = get_headers(jwt = jwt)
    else:
        headers = get_headers(without_token = True)

    return requests.get(api_url, json = data, headers = headers)

def post_mark(poem_id, score, comment, user_id):
    api_url = f'{current_app.config["API_URL"]}/marks'

    data = {"score": score, "comment":comment, "userID":user_id, "poemID":poem_id}
    headers = get_headers()
    return requests.post(api_url, json = data, headers = headers)
# -- Marks --

# -- json --
def get_json(resp):
    return json.loads(resp.text)
# -- json --

# -- Auth --
def login(email, password):
    api_url = f'{current_app.config["API_URL"]}/auth/login'

    # Envio de logueo.
    data = {"email": email, "password": password}
    headers = get_headers(without_token = True)

    # Generamos la respuesta, mandando endpoint, data diccionario, y el headers que es el formato como aplication json.
    return requests.post(api_url, json = data, headers = headers)

def register(name, email, password):
    api_url = f'{current_app.config["API_URL"]}/auth/register'

    # Envio de logueo.
    data = {"name": name, "email": email, "password": password, "rol": "user"}
    headers = get_headers(without_token = True)

    # Generamos la respuesta, mandando endpoint, data diccionario, y el headers que es el formato como aplication json.
    return requests.post(api_url, json = data, headers = headers)

def get_headers(without_token = False, jwt = None):
    if jwt == None and without_token == False:
        return {"Content-Type" : "application/json", "Authorization" : f"Bearer {get_jwt()}"}
    if jwt and without_token == False:
        return {"Content-Type" : "application/json", "Authorization" : f"Bearer {jwt}"}
    else:
        return {"Content-Type" : "application/json"}

def get_jwt():
    token = request.cookies.get("access_token")
    expired = auth.check_jwt_expiration(token)
    if (expired):
        return None
    else:
        return token
# -- Auth --

