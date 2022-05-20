from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import UserModel
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from main.auth.decorators import admin_required

#Recurso Usuario
class User(Resource):
    #Obtener un Usuario
    @jwt_required(optional=True) #Requisito para todos los usuarios tanto con token como no.
    def get(self, id):

        #Obtener claims de adentro del JWT
        claims = get_jwt()

        user = db.session.query(UserModel).get_or_404(id)

        #Verifico si no tiene token, devuelvo el json para un usuario no registrado.
        if (not claims):
            return user.to_json()

        #Verificar que el rol sea admin y devuelvo el mail, sino devuelvo normal para el user.
        if (claims['role'] == "admin"):
            return user.to_json_admin()
        elif (claims['role'] == "user"):
            return user.to_json_user()
        else:
            return user.to_json()
            
    
    #Eliminar un Usuario
    @jwt_required() #Requisito de admin o usuario para ejecutar esta función. Obligatorio Token
    def delete(self, id):

        #Obtener claims de adentro del JWT
        claims = get_jwt()

        #Verifico si el id del usuario concuerda con el que realiza el deleteo o si es admin.
        if (claims['id'] == id or claims['role'] == "admin"):
            user = db.session.query(UserModel).get_or_404(id)
            db.session.delete(user)
            db.session.commit()
            return '', 204 #Elemento eliminado correctamente.
        else:
            return 'No tiene rol', 403 #La solicitud no incluye información de autenticación

    #Modificar un usuario
    @jwt_required() #Requisito de admin o usuario para ejecutar esta función. Obligatorio Token
    def put(self, id):

        #Obtener claims de adentro del JWT
        claims = get_jwt()

        #Verifico si el id del usuario concuerda con el que realiza la modificación o si es admin.
        if (claims['id'] == id): #or claims['role'] == "admin"):
            user = db.session.query(UserModel).get_or_404(id)
            data = request.get_json().items()
            for key, value in data:
                setattr(user, key, value)
            db.session.add(user)
            db.session.commit()
            return user.to_json_user(), 201
        else:
            return 'No tiene rol', 403 #La solicitud no incluye información de autenticación

#Recurso Usuarios
class Users(Resource):
    #Obtener Lista de Usuarios
    @admin_required #Solo admines pueden acceder.
    def get(self):
        # En caso de que el usuario no especifique pagina.
        page = 1

        users = db.session.query(UserModel)
        if request.get_json():
            filters = request.get_json().items()
            for key, value in filters:
                # Pagina actual que se encuentra el usuario.
                if key == "page":
                    page = int(value)
                # Cantidad de elementos que queres que te traiga por pagina.
                if key == "perpage":
                    perpage = int(value)
                # Traer la lista por nombre especifico.
                if key == "name":
                    users = users.filter(UserModel.name.like("%" + value + "%"))
                # Ordenar toda la tabla de usuarios ordenados por:
                if key == "sort_by":
                    # Ordenado por nombre ascendente
                    if value == "name":
                        users = users.order_by(UserModel.name)
                    # Ordenado por nombre descendente
                    if value == "name[desc]":
                        users = users.order_by(UserModel.name.desc())
                
        users = users.paginate(page, perpage, True, 10)
        return jsonify({"users":[user.to_json() for user in users.items],
        "total": users.total, "pages": users.pages, "page": page})

    @admin_required #Solo admines pueden acceder.
    #Agregar un nuevo Usuario en la lista
    def post(self):
        user = UserModel.from_json(request.get_json())
        db.session.add(user)
        db.session.commit()
        return user.to_json(), 201
