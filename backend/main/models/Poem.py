from .. import db
from datetime import datetime

class Poem(db.Model):

    # Generamos las columnas de Usuario
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    userID = db.Column(db.Integer, nullable=False) # ToDo: Ver si hacer esto clave foranea.
    body = db.Column(db.String(100), nullable=False)
    created_at = db.Column(datetime.now(), nullable=False) # ToDo: Ver como obtener el datetime desde la base de datos

    # Debuger, mostrar contenido de la tabla.
    def __repr__(self):
        return f"<Poem {self.title} {self.userID} {self.body} {self.created_at} >"

    #Convertir objeto en JSON
    def to_json(self):
        poem_json = {
            'id': self.id,
            'title': str(self.title),
            'userID': int(self.userID),
            'body': str(self.body),
            'created_at': str(self.created_at),
        }
        return poem_json
    
    @staticmethod
    #Convertir JSON a objeto
    def from_json(poem_json):
        id = poem_json.get('id')
        title = poem_json.get('title')
        userID = poem_json.get('userID')
        body = poem_json.get('body')
        created_at = poem_json.get('created_at')
        return Poem(id=id,
                    title=title,
                    userID=userID,
                    body=body,
                    created_at=created_at
                    )
