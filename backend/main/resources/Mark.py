from flask_restful import Resource
from flask import request

#Diccionario de prueba
MARKS = {
    1: {'mark': '5 estrellas'},
    2: {'mark': '3 estrellas'},
}

# Recurso Calificacion
class Mark(Resource):
    #Obtener una Calificacion
    def get(self, id):
        if int(id) in MARKS:
            return MARKS[int(id)]
        return '', 404
    
    #Eliminar una calificacion
    def delete(self, id):
        if int(id) in MARKS:
            del MARKS[int(id)]
            return '', 204
        return '', 404

# Recurso Calificaciones
class Marks(Resource):
    #Obtener Lista de Calificaciones
    def get(self):
        if MARKS:
            return MARKS
        return '', 404

    #Agregar una Calificacion a la lista 
    def post(self):
        mark = request.get_json()
        id = int(max(MARKS.keys())) + 1
        MARKS[id] = mark
        return MARKS[id], 201
