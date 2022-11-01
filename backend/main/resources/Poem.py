from datetime import datetime
from itertools import count
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

        #Obtener claims de adentro del JWT
        claims = get_jwt()

        poem = db.session.query(PoemModel).get_or_404(id)

        #Verifico si no tiene token, devuelvo el json para un usuario no registrado.
        if (not claims):
            return poem.to_json()

        #Verificar que el rol sea admin y devuelvo el mail, sino devuelvo normal para el user.
        if (claims['role'] == "admin"):
            return poem.to_json_admin()
        elif (claims['role'] == "user"):
            return poem.to_json_user()
        else:
            return poem.to_json()
    
    #Eliminar un Poema
    @jwt_required() #Requisito de admin o usuario para ejecutar esta función. Obligatorio Token
    def delete(self, id):

        #Obtener claims de adentro del JWT
        claims = get_jwt()

        poem = db.session.query(PoemModel).get_or_404(id)

        #Verifico si el id del usuario concuerda con el que realiza el deleteo o si es admin.
        if (claims['id'] == poem.userID or claims['role'] == "admin"):
            db.session.delete(poem)
            db.session.commit()
            return 'Elemento eliminado', 204 #Elemento eliminado correctamente.
        elif (claims['id'] != poem.userID):
            return 'No puede eliminar un poema ajeno', 404
        else:
            return 'No tiene rol', 403 #La solicitud no incluye información de autenticación

            
#Recurso Poemas
class Poems(Resource):
    #Obtener Recurso
    @jwt_required(optional=True) #Requisito para todos los usuarios tanto con token como no.
    def get(self):

        #Obtener claims de adentro del JWT
        claims = get_jwt()

        #Verifico si no tiene token, devuelvo lista de poemas sin ordenamiento.
        if (not claims):
            return self.ShowPoemsWithoutToken()

        if (claims['role'] == "user" or "admin"):
            return self.ShowPoemsWithToken(userID = claims['id'])
        else:
            return 'No tiene rol', 403 #La solicitud no incluye información de autenticación
    
    #Agregara un nuevo Poema a la lista
    @jwt_required() #Requisito de admin o usuario para ejecutar esta función. Obligatorio Token
    def post(self):

        #Obtener claims de adentro del JWT
        claims = get_jwt()

        #Verifico si el id del usuario concuerda con el que realiza la modificación o si es admin.
        if (claims['role'] == "user" or "admin"):

            #Cancelar operacion en caso de que el id del request y del jwt sean diferentes
            #if (claims['id'] != request.get_json().get('id')):
            #    return 'El id de consulta no coincide con el de su cuenta', 404

            # Me traigo el usuario por el id.
            user = db.session.query(UserModel).get_or_404(claims['id'])

            # Condición para poder publicar su primer poema
            if (len(user.poems) == 0 or len(user.marks)/len(user.poems) >= 0):
                poem = PoemModel.from_json(request.get_json())
                db.session.add(poem)
                db.session.commit()
                if (claims['role'] == "admin"):
                    return poem.to_json_admin(), 201
                elif (claims['role'] == "user"):
                    return poem.to_json_user(), 201
            else:
                return 'No cumple las condiciones', 404 #Error al intentar publicar y no cumplir la condición de poemas publicados
        else:
            return 'No tiene rol', 403 #La solicitud no incluye información de autenticación


    # Utils functions.
    # Mostrar poemas con ordenamiento para poetas y admines.
    def ShowPoemsWithoutToken(self):
        
        # En caso de que el usuario no especifique pagina.
        page = 1

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
                    poems = poems.filter(PoemModel.user.has(UserModel.name.like("%" + value + "%")))
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

    def ShowPoemsWithToken(self, userID):

        # En caso de que el usuario no especifique pagina.
        page = 1

        # Me traigo los poemas que no publico el usuario y ordenado por calificaciones.
        poems = db.session.query(PoemModel).filter(PoemModel.userID != int(userID)).order_by(PoemModel.created_at).outerjoin(PoemModel.marks).group_by(PoemModel.id).order_by(func.count(MarkModel.score))

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