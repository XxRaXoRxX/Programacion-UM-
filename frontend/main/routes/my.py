from flask import Blueprint, current_app, redirect, url_for, render_template, request, make_response
from . import functions as func
from . import auth as auth
import requests
import json

#Crear Blueprint
my = Blueprint('my', __name__, url_prefix='/my')

# Ver información del usuario
@my.route('/')
def index():
    # traemos el token de las cookies.
    jwt = func.get_jwt()

    if (jwt):
        user = auth.load_user(jwt)
        
        # Guardamos la información de usuario en una variable.
        user_info = func.get_user_info(user["id"])
        user_info = json.loads(user_info.text)

        resp = make_response(render_template('user_info.html', jwt = jwt, user_info = user_info))
        func.reset_page_cookie(resp)
        return resp
    else:
        resp = make_response(redirect(url_for('main.login')))
        func.reset_page_cookie(resp)
        return resp

# Ver poemas del usuario
@my.route('/poems', methods=['GET', 'POST'])
def poems():

    jwt = func.get_jwt()
    if (jwt):

        # Filtros
        filter_title = request.form.get("filter_title")
        filter_rating = request.form.get("filter_rating")

        # Usuario
        user = auth.load_user(jwt)

        # Paginacion
        try:
            page = int(request.form.get("_page"))
        except:
            page = request.form.get("_page")
            if (page == "< Atras"):
                page = int(func.get_poems_page()) - 1
            elif (page == "Siguiente >"):
                page = int(func.get_poems_page()) + 1
            else:
                page = func.get_poems_page()
                if (page == None):
                    page = 1
                else:
                    page = int(page)

        if(request.method == "POST" and (filter_title != "" or filter_rating != None)):
            # Obtener los poemas.
            resp = func.get_poems_by_id(id = user["id"],
                                        title = filter_title, 
                                        rating = filter_rating, 
                                        page = page)

        else:
            resp = func.get_poems_by_id(id = user["id"], page = int(page))

        # Guardamos los poemas en una variable.
        poems = json.loads(resp.text)
        poemsList = poems["poems"]

        resp = make_response(render_template('user_poems.html', 
                                              jwt = jwt, 
                                              poems = poemsList, 
                                              page = page,
                                              filter_title = filter_title,
                                              filter_rating = filter_rating))
        resp.set_cookie("poems_page", str(page))
        return resp
    else:
        resp = make_response(redirect(url_for('main.login')))
        func.reset_page_cookie(resp)
        return resp

# Editar usuario
@my.route('/edit', methods=['GET', 'POST'])
def edit():

    jwt = func.get_jwt()

    if(request.method == "POST"):
        if (jwt):
            # Obtener el nuevo nickname
            nick = request.form.get("editar_nick")
            
            user = auth.load_user(jwt)

            if nick != "":
                # Cambiar nombre de usuario en la base de datos.
                resp = func.put_username(user["id"], nick)

                # Guardamos la información de usuario en una variable.
                user_info = func.get_user_info(user["id"])
                user_info = json.loads(user_info.text)

                if (resp.ok):
                    resp = make_response(render_template('user_config.html', jwt = jwt, user = user_info, success = "Nombre de usuario cambiado correctamente"))
                    func.reset_page_cookie(resp)
                    return resp
                else:
                    resp = make_response(render_template('user_config.html', jwt = jwt, user = user_info, error = "No se ha podido cambiar el nombre de usuario"))
                    func.reset_page_cookie(resp)
                    return resp
            else:
                # Guardamos la información de usuario en una variable.
                user_info = func.get_user_info(user["id"])
                user_info = json.loads(user_info.text)

                resp = make_response(render_template('user_config.html', jwt = jwt, user = user_info, error = "El nombre de usuario no puede estar vacío")       )
                func.reset_page_cookie(resp)
                return resp
    else:   
        if (jwt):
            user = auth.load_user(jwt)

            # Guardamos la información de usuario en una variable.
            user_info = func.get_user_info(user["id"])
            user_info = json.loads(user_info.text)

            resp = make_response(render_template('user_config.html', jwt = jwt, user = user_info))
            func.reset_page_cookie(resp)
            return resp
    
    return redirect(url_for('main.login'))

# Eliminar cuenta del usuario
@my.route('/delete', methods=['GET', 'POST'])
def delete():

    jwt = func.get_jwt()

    if (jwt):

        if(request.method == "POST"):
        
            user = auth.load_user(jwt)

            resp = func.delete_user(user_id = user["id"], jwt = jwt)

            if (resp.ok):
                return make_response(redirect(url_for('main.logout')))
            else:
                resp = make_response(render_template('delete_account.html', error = "Error al eliminar el usuario"))
                func.reset_page_cookie(resp)
                return resp

    resp = make_response(render_template('delete_account.html'))
    func.reset_page_cookie(resp)
    return resp

# Cambiar contraseña del usuario
@my.route('/password', methods=['GET', 'POST'])
def password():
    jwt = func.get_jwt()

    if(request.method == "POST"):
        if (jwt):
            # Obtener la nueva contraseña
            actual_pass = request.form.get("actual_password")
            new_pass = request.form.get("new_password")
            
            # Obtener datos del usuario
            user = auth.load_user(jwt)
            email = user["email"]

            if email != "" and actual_pass != "":
                response = func.login(email, actual_pass)
            
                if (response.ok):
                    # Cambiar contraseña en la base de datos.
                    resp = func.put_password(user["id"], new_pass)

                    if (resp.ok):
                        resp = make_response(render_template('change_password.html', jwt = jwt, success = "Contraseña cambiada correctamente"))
                        func.reset_page_cookie(resp)
                        return resp

            resp = make_response(render_template('change_password.html', jwt = jwt, error = "No se ha podido cambiar la contraseña"))
            func.reset_page_cookie(resp) 
            return resp
    else:
        if (jwt):
            resp = make_response(render_template('change_password.html', jwt = jwt))
            func.reset_page_cookie(resp)
            return resp
    
    return redirect(url_for('main.login'))