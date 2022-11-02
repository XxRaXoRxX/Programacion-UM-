from flask import Blueprint, redirect, url_for, render_template, request, current_app
from . import functions as func
from . import auth as auth
import requests

#Crear Blueprint
poem = Blueprint('poem', __name__, url_prefix='/poem')

# Ver un poema determinado.
@poem.route('/view/<int:id>', methods=['GET', 'POST'])
def view(id):

    jwt = func.get_jwt()

    if(request.method == "POST"):
        if (jwt):
            # Postear comentario.
            user = auth.load_user(jwt)
            user_id = user["id"]
            score = request.form.get("score")
            comment = request.form.get("comentario")
            resp = func.post_mark(poem_id = id, score = score, comment = comment, user_id = user_id)

            # Obtener el poema y los comentarios.
            poem, marks = get_poem_and_marks(id)

            if (resp.ok):
                return render_template('poems.html', jwt = jwt, poem = poem, marks = marks, message = "Comentario publicado con éxito.")
            else:
                # TODO: Mostrar error.
                return render_template('poems.html', jwt = jwt, poem = poem, marks = marks, message = "Error al publicar el comentario.")

    else:
        if (jwt):

            poem, marks = get_poem_and_marks(id)
            return render_template('poems.html', jwt = jwt, poem = poem, marks = marks)

    return redirect(url_for('main.login'))

def get_poem_and_marks(poem_id):
    # Obtener el poema.
    resp = func.get_poem(poem_id)
    poem = func.get_json(resp)
    # Obtener los comentarios.
    resp = func.get_marks_by_poem_id(poem_id)
    marks = func.get_json(resp)

    return poem, marks

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