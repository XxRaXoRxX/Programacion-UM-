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

        resp = func.get_marks_by_poem_id(id)
        marks = func.get_json(resp)

        return render_template('poems.html', jwt = jwt, poem = poem, marks = marks)
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

            if titulo_poema != "" and cuerpo_poema != "":
                
                user = auth.load_user(jwt)

                response = func.create_poem(id = user["id"], 
                                            titulo_poema = titulo_poema, 
                                            cuerpo_poema = cuerpo_poema)

                if (response.ok):
                    # Traer poema y mostrarlo.
                    resp = func.get_json(response)
                    id = resp["id"]
                    return view(id)
            
            # TODO: Mostrar mensaje de error al crear poema.
            return render_template("create_poem.html", jwt = jwt)
    else:
        if (jwt):
            return render_template('create_poem.html', jwt = jwt)

    return redirect(url_for('main.login'))