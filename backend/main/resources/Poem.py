from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import PoemModel

#Diccionario de prueba
POEMS = {
    1: {'title': 'El Libertario', 'autor': 'ElPelucaMilei'},
    2: {'title': 'Aventurero frustrado por flecha en rodilla', 'autor': 'Guardia de Skyrim'},
}

#Recurso Poema
class Poem(Resource):
    #Obtener un Poema
    def get(self, id):
        poem = db.session.query(PoemModel).get_or_404(id)
        return poem.to_json()
    
    #Eliminar un Poema
    def delete(self, id):
        poem = db.session.query(PoemModel).get_or_404(id)
        db.session.delete(poem)
        db.session.commit()
        return '', 204

            
#Recurso Poemas
class Poems(Resource):
    #Obtener Recurso
    def get(self):
        poems = db.session.query(PoemModel).all()
        return jsonify([poem.to_json() for poem in poems])
    
    #Agregara un nuevo Poema a la lista
    def post(self):
        poem = PoemModel.from_json(request.get_json())
        db.session.add(poem)
        db.session.commit()
        return poem.to_json(), 201