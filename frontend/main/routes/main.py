from flask import Blueprint, redirect, url_for, render_template

#Crear Blueprint
main = Blueprint('main', __name__, url_prefix='/')

# Ruta menu principal con poemas
@main.route('/')
def index():
    return render_template('main.html')

# Ruta menu principal con poemas
@main.route('/login')
def login():
    return render_template('login.html')
