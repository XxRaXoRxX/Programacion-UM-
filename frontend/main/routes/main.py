from flask import Blueprint, redirect, url_for

#Crear Blueprint
main = Blueprint('main', __name__, url_prefix='/')

# Ruta menu principal con poemas
@main.route('/')
def index():
    return redirect(url_for('main.html'))

# Ruta menu principal con poemas
@main.route('/login')
def index():
    return redirect(url_for('login.html'))
