from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import UserModel

#Recurso Usuario
class User(Resource):
    #Obtener un Usuario
    def get(self, id):
        user = db.session.query(UserModel).get_or_404(id)
        return user.to_json()
    
    #Eliminar un Usuario
    def delete(self, id):
        user = db.session.query(UserModel).get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        return '', 204

    #Modificar un usuario
    def put(self, id):
        user = db.session.query(UserModel).get_or_404(id)
        data = request.get_json().items()
        for key, value in data:
            setattr(user, key, value)
        db.session.add(user)
        db.session.commit()
        return user.to_json(), 201

#Recurso Usuarios
class Users(Resource):
    #Obtener Lista de Usuarios
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

    #Agregar un nuevo Usuario en la lista
    def post(self):
        user = UserModel.from_json(request.get_json())
        db.session.add(user)
        db.session.commit()
        return user.to_json(), 201
