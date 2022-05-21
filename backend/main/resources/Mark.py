from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import MarkModel
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from main.auth.decorators import admin_required
from main.mail.functions import sendMail

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

    #Editar una calificación
    #ToDo: Consideramos que no se puede editar una calificación en las primeras clases, de todas formas considero que si debería poder editarse.
    #En caso de que un usuario se equivoque, o en un futuro quiere cambiar su calificación.
    #Modificar un usuario
    @jwt_required() #Requisito de admin o usuario para ejecutar esta función. Obligatorio Token
    def put(self, id):
    
        #Obtener claims de adentro del JWT
        claims = get_jwt()
    
        mark = db.session.query(MarkModel).get_or_404(id)

        #Verifico si el id del usuario concuerda con el que realiza la modificación o si es admin.
        if (claims['id'] == mark.user.id): #or claims['role'] == "admin"):
            data = request.get_json().items()
            for key, value in data:
                setattr(mark, key, value)
            db.session.add(mark)
            db.session.commit()
            return mark.to_json_user(), 201
        elif (claims['id'] != id):
            return 'No puedes editar una calificación ajena', 404
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

        #Cancelar operacion en caso de que el id del request y del jwt sean diferentes
        if (claims['id'] != request.get_json().get('userID')):
            return 'El id de consulta no coincide con el de su cuenta', 404

        #Verifico si es un usuario el que quiere postear las calificaciones.
        #ToDo: El admin no se considero en este caso, que sucede si hay un admin que es poeta?, yo lo incluyo por un tema de testeo y por la respuesta
        #a la pregunta anterior, no tiene sentido que un admin que es poeta tenga que tener dos cuentas para poder realizar cosas.
        if (claims['role'] == "user" or claims['role'] == "admin"):
            mark = MarkModel.from_json(request.get_json())
            db.session.add(mark)
            db.session.commit()

            #Envio de mail al creador del poema.
            subject = "Calificación recibida en poema " + str(mark.poem.title)
            email = sendMail(to = [mark.poem.user.email], subject = subject, template = "mark", mark = mark)
            return mark.to_json(), 201 #Finaliza correctamente la operación
        else:
            return 'No tiene rol', 403 #La solicitud no incluye información de autenticación
