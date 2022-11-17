from flask import Blueprint, redirect, url_for, render_template, request, current_app, make_response
from . import functions as func
from . import auth as auth
import requests

#Crear Blueprint
poem = Blueprint('poem', __name__, url_prefix='/poem')

# Ver un poema determinado.
@poem.route('/view/<int:id>', methods=['GET', 'POST', 'DELETE'])
def view(id):

    jwt = func.get_jwt()
    user = auth.load_user(jwt)

    # Borrar el poema.
    if (request.method == "POST" and request.form.get("_method") == "DELETE"):
        if (jwt):

            poem, marks = get_poem_and_marks(id, jwt = jwt)

            if (request.form.get("_delete") == "yes"):
                # Eliminar poema.
                resp = func.delete_poem(poem_id = id, jwt = jwt)

                if (resp.ok):
                    return redirect(url_for('main.index'))
                else:
                    # TODO: Mostrar error.
                    return render_template('poem.html', jwt = jwt, user = user, poem = poem, marks = marks, error = "Error al eliminar el poema.")
            else:
                return render_template("delete_poem.html", jwt = jwt, poem = poem)
            

    # Postear comentario.
    elif (request.method == "POST"):
        if (jwt):
            score = request.form.get("score")
            comment = request.form.get("comentario")
            resp = func.post_mark(poem_id = id, score = score, comment = comment, user_id = user["id"])

            # Obtener el poema y los comentarios.
            poem, marks = get_poem_and_marks(poem_id = id, jwt = jwt)

            if (resp.ok):
                return render_template('poem.html', jwt = jwt, user = user, poem = poem, marks = marks, success = "Comentario publicado con éxito.")
            else:
                # TODO: Mostrar error.
                return render_template('poem.html', jwt = jwt, user = user, poem = poem, marks = marks, error = "Error al publicar el comentario.")

    else:
        poem, marks = get_poem_and_marks(id, jwt = jwt)
        return render_template('poem.html', jwt = jwt, user = user, poem = poem, marks = marks)

    return redirect(url_for('main.login'))

def get_poem_and_marks(poem_id, jwt = None):
    # Obtener el poema.
    resp = func.get_poem(poem_id, jwt)
    poem = func.get_json(resp)
    # Obtener los comentarios.
    resp = func.get_marks(poem_id, jwt)
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
                    return make_response(redirect(url_for('poem.view', id=id)))
            
            # TODO: Mostrar mensaje de error al crear poema.
            return render_template("create_poem.html", jwt = jwt)
    else:
        if (jwt):
            return render_template('create_poem.html', jwt = jwt)

    return redirect(url_for('main.login'))

# Editar un poema.
@poem.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    jwt = func.get_jwt()

    # Editar el poema.
    if (request.method == "POST"):
        if (jwt):
            titulo_poema = request.form.get("titulo_poema")
            cuerpo_poema = request.form.get("cuerpo_poema")

            if titulo_poema != "" and cuerpo_poema != "":
                resp = func.edit_poem(id = id, 
                                      titulo_poema = titulo_poema, 
                                      cuerpo_poema = cuerpo_poema)

                if (resp.ok):
                    return make_response(redirect(url_for('poem.view', id=id)))
                else:
                    # TODO: Mostrar mensaje de error al crear poema.
                    poem = func.get_poem(id, jwt)
                    poem = func.get_json(poem)
                    return render_template("edit_poem.html", jwt = jwt, poem = poem, error = "Error al editar el poema.")

    else:
        poem = func.get_poem(id, jwt)
        poem = func.get_json(poem)
        print(poem)
        return render_template('edit_poem.html', jwt = jwt, poem = poem)

    return redirect(url_for('main.login'))