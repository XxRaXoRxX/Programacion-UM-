from flask_restful import Resource
from flask import request

#Diccionario de prueba
USERS = {
    1: {'name': 'Roberto', 'surname': 'Martinez'},
    2: {'name': 'Juan', 'surname': 'Sanchez'},
}

#Recurso Usuario
class User(Resource):
    #Obtener un Usuario
    def get(self, id):
        if int(id) in USERS:
            return USERS[int(id)]
        return '', 404
    
    #Eliminar un Usuario
    def delete(self, id):
        if int(id) in USERS:
            del USERS[int(id)]
            return '', 204
        return '', 404

    #Modificar un usuario
    def put(self, id):
        if int(id) in USERS:
            user = USERS[int(id)]
            #Obtengo los datos de la solicitud
            data = request.get_json()
            user.update(data)
            return user, 201
        return '', 404
    

#Recurso Usuarios
class Users(Resource):
    #Obtener Lista de Usuarios
    def get(self):
        if USERS:
            return USERS
        return '', 404

    #Agregar un nuevo Usuario en la lista
    def post(self):
        user = request.get_json()
        id = int(max(USERS.keys())) + 1
        USERS[id] = user
        return USERS[id], 201
