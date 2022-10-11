from flask import Blueprint, redirect, url_for, render_template, make_response, request
import requests
import json

def get_poems(api_url, page = 1, perpage = 3):
    # Envio de la pagina y cuantos datos por pagina.
    data = {"page": page, "perpage": perpage}

    # Obtengo el jwt del logueo e instancio headers y le agrego el jwt.
    headers = get_headers()

    # Creamos el response y le enviamos el data y headers.
    return requests.get(api_url, json = data, headers = headers)

def get_headers():
    return {"Content-Type" : "application/json", "Authorization" : f"BEARER {get_jwt()}"}

def get_jwt():
    return request.cookies.get("access_token")