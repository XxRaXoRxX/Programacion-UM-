from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import MarkModel
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from main.auth.decorators import admin_required

# Recurso Calificacion
class Mark(Resource):
    #Obtener una Calificacion
    @jwt_required(optional=True) #Requisito para todos los usuarios tanto con token como no.
    def get(self, id):
        mark = db.session.query(MarkModel).get_or_404(id)
        return mark.to_json()
    
    #Eliminar una calificacion
    @jwt_required() #Requisito de admin o usuario para ejecutar esta función. Obligatorio Token
    def delete(self, id):

        #Obtener claims de adentro del JWT
        claims = get_jwt()

        #Verifico si el id del usuario concuerda con el que realiza la modificación o si es admin.
        if (claims['id'] == id or claims['role'] == "admin"):
            mark = db.session.query(MarkModel).get_or_404(id)
            db.session.delete(mark)
            db.session.commit()
            return '', 204 #Elemento eliminado correctamente.
        else:
            return 'No tiene rol', 403 #La solicitud no incluye información de autenticación

# Recurso Calificaciones
class Marks(Resource):
    #Obtener Lista de Calificaciones
    @jwt_required(optional=True) #Requisito para todos los usuarios tanto con token como no.
    def get(self):
        marks = db.session.query(MarkModel).all()
        return jsonify([mark.to_json() for mark in marks])

    #Agregar una Calificacion a la lista 
    @jwt_required() #Requisito de admin o usuario para ejecutar esta función. Obligatorio Token
    def post(self):

        #Obtener claims de adentro del JWT
        claims = get_jwt()

        #Verifico si es un usuario el que quiere postear las calificaciones.
        if (claims['role'] == "user"):
            mark = MarkModel.from_json(request.get_json())
            db.session.add(mark)
            db.session.commit()
            return mark.to_json(), 201 #Finaliza correctamente la operación
        else:
            return 'No tiene rol', 403 #La solicitud no incluye información de autenticación
