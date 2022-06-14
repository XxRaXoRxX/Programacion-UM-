from flask import Blueprint, redirect, url_for

#Crear Blueprint
poem = Blueprint('poem', __name__, url_prefix='/poem')

# Ver un poema determinado.
@poem.route('/view/<int:id>')
def view(id):
    return redirect(url_for('poems.html'))

# Crear un nuevo poema.
@poem.route('/create')
def create():
    return redirect(url_for('create_poem.html'))