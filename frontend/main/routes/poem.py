from flask import Blueprint, redirect, url_for, render_template

#Crear Blueprint
poem = Blueprint('poem', __name__, url_prefix='/poem')

# Ver un poema determinado.
@poem.route('/view/<int:id>')
def view(id):
    return render_template('poems.html')

# Crear un nuevo poema.
@poem.route('/create')
def create():
    return render_template('create_poem.html')