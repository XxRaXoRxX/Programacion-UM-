from flask import Blueprint, redirect, url_for, render_template, request, current_app
from . import functions as func
from . import auth as auth
import requests

#Crear Blueprint
poem = Blueprint('poem', __name__, url_prefix='/poem')

# Ver un poema determinado.
@poem.route('/view/<int:id>')
def view(id):
    jwt = func.get_jwt()

    if (jwt):
        resp = func.get_poem(id)
        poem = func.get_json(resp)

        return render_template('poems.html', jwt = jwt, poem = poem)
    else:
        return redirect(url_for('main.login'))

# Crear un nuevo poema.
@poem.route('/create', methods=['GET', 'POST'])
def create():

    jwt = func.get_jwt()

    if(request.method == "POST"):
        if (jwt):
            titulo_poema = request.form.get("titulo_poema")
            cuerpo_poema = request.form.get("cuerpo_poema")

            if titulo_poema != None and cuerpo_poema != None:
                
                user = auth.load_user(jwt)

                response = func.create_poem(titulo_poema, cuerpo_poema, user["id"])

                if (response.ok):
                    return render_template("poems.html", jwt = jwt)
            
            # TODO: Mostrar mensaje de error al crear poema.
            return render_template("create_poem.html", jwt = jwt)
    else:
        if (jwt):
            return render_template('create_poem.html', jwt = jwt)

    return redirect(url_for('main.login'))