from flask_restful import Resource
from flask import request

#Diccionario de prueba
POEMS = {
    1: {'title': 'El Libertario', 'autor': 'ElPelucaMilei'},
    2: {'title': 'Aventurero frustrado por flecha en rodilla', 'autor': 'Guardia de Skyrim'},
}

#Recurso Poema
class Poem(Resource):
    #Obtener un Poema
    def get(self, id):
        if int(id) in POEMS:
            return POEMS[int(id)]
        return '', 404
    
    #Eliminar un Poema
    def delete(self, id):
        if int(id) in POEMS:
            del POEMS[int(id)]
            return '', 204
        return '', 404

            
#Recurso Poemas
class Poems(Resource):
    #Obtener Recurso
    def get(self):
        if POEMS:
            return POEMS
        return '', 404
    
    #Agregara un nuevo Poema a la lista
    def post(self):
        poem = request.get_json()
        id = int(max(POEMS.keys())) + 1
        POEMS[id] = poem
        return POEMS[id], 201