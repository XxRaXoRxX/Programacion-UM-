from datetime import datetime
from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import PoemModel
from main.models import UserModel
from main.models import MarkModel
from sqlalchemy import func
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from main.auth.decorators import admin_required

#Recurso Poema
class Poem(Resource):
    #Obtener un Poema
    @jwt_required(optional=True) #Requisito para todos los usuarios tanto con token como no.
    def get(self, id):
        poem = db.session.query(PoemModel).get_or_404(id)
        return poem.to_json()
    
    #Eliminar un Poema
    @jwt_required() #Requisito de admin o usuario para ejecutar esta función. Obligatorio Token
    def delete(self, id):

        #Obtener claims de adentro del JWT
        claims = get_jwt()

        #Verifico si el id del usuario concuerda con el que realiza el deleteo o si es admin.
        if (claims['id'] == id or claims['role'] == "admin"):
            poem = db.session.query(PoemModel).get_or_404(id)
            db.session.delete(poem)
            db.session.commit()
            return '', 204 #Elemento eliminado correctamente.
        else:
            return '', 401 #La solicitud no incluye información de autenticación

            
#Recurso Poemas
class Poems(Resource):
    #Obtener Recurso
    @jwt_required(optional=True) #Requisito para todos los usuarios tanto con token como no.
    def get(self):

        # En caso de que el usuario no especifique pagina.
        page = 1

        #Obtener claims de adentro del JWT
        claims = get_jwt()

        #Verifico si no tiene token, devuelvo lista de poemas sin ordenamiento.
        if (not claims):
            return self.ShowPoemsWithoutToken()

        if (claims['role'] == "user" or "admin"):
            return self.ShowPoemsWithToken()
        else:
            return '', 401 #La solicitud no incluye información de autenticación
    
    #Agregara un nuevo Poema a la lista
    @jwt_required() #Requisito de admin o usuario para ejecutar esta función. Obligatorio Token
    def post(self):

        #Obtener claims de adentro del JWT
        claims = get_jwt()

        #Verifico si el id del usuario concuerda con el que realiza la modificación o si es admin.
        if (claims['role'] == "user" or "admin"):
            poem = PoemModel.from_json(request.get_json())
            db.session.add(poem)
            db.session.commit()
            return poem.to_json(), 201
        else:
            return '', 401 #La solicitud no incluye información de autenticación


    # Utils functions.

    # Mostrar poemas con ordenamiento para poetas y admines.
    def ShowPoemsWithToken():
        poems = db.session.query(PoemModel)
        if request.get_json():
            filters = request.get_json().items()
            for key, value in filters:
                # Pagina actual que se encuentra el usuario.
                if key == "page":
                    page = int(value)
                # Cantidad de elementos que queres que te traiga por pagina.
                if key == "perpage":
                    perpage = int(value)
                # Traer por nombre de titulo.
                if key == "title":
                    # "%" Sirve para traer cualquier otro caracter despues y antes de value.
                    poems = poems.filter(PoemModel.title.like("%" + value + "%"))
                # Traer poemas por id de usuario.
                if key == "userID":
                    poems = poems.filter(PoemModel.userID == value)
                # Traer poemas mayor al tiempo ingresado.
                if key == "date_time[gte]":
                    poems = poems.filter(PoemModel.created_at >= datetime.strptime(value, "%d/%m/%Y"))
                # Traer poemas menor al tiempo ingresado
                if key == "date_time[lte]":
                    poems = poems.filter(PoemModel.created_at <= datetime.strptime(value, "%d/%m/%Y"))
                # Traer poemas por nombre de usuario.
                if key == "username":
                    poems = poems.filter(PoemModel.user.has(UserModel.username.like("%" + value + "%")))
                # Traer poemas por rating
                if key == "rating":
                    poems = poems.outerjoin(PoemModel.marks).group_by(PoemModel.id).having(func.avg(MarkModel.score).like(float(value)))
                # Ordenar toda la tabla de poemas ordenados por:
                if key == "sort_by":
                    # Ordenado por tiempo
                    if value == "date_time":
                        poems = poems.order_by(PoemModel.created_at)
                    # Ordenado por tiempo descendiente
                    if value == "date_time[desc]":
                        poems = poems.order_by(PoemModel.created_at.desc())
                    # Ordenado por calificaciones.
                    if value == "mark":
                        poems = poems.outerjoin(PoemModel.marks).group_by(PoemModel.id).order_by(func.count(MarkModel.score))
                    # Ordenado por calificaciones descendiente.
                    if value == "mark[desc]":
                        poems = poems.outerjoin(PoemModel.marks).group_by(PoemModel.id).order_by(func.count(MarkModel.score).desc())
                
        poems = poems.paginate(page, perpage, True, 10)
        return jsonify({"poems":[poem.to_json() for poem in poems.items],
        "total": poems.total, "pages": poems.pages, "page": page})

    # Mostrar poemas con ordenamiento para poetas y admines.
    def ShowPoemsWithoutToken():
        poems = db.session.query(PoemModel)
        if request.get_json():
            filters = request.get_json().items()
            for key, value in filters:
                # Pagina actual que se encuentra el usuario.
                if key == "page":
                    page = int(value)
                # Cantidad de elementos que queres que te traiga por pagina.
                if key == "perpage":
                    perpage = int(value)

        poems = poems.paginate(page, perpage, True, 10)
        return jsonify({"poems":[poem.to_json() for poem in poems.items],
        "total": poems.total, "pages": poems.pages, "page": page})

    # Utils functions.