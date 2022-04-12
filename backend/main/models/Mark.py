from .. import db

class Mark(db.Model):

    # Generamos las columnas de Usuario
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(100), nullable=False) 
    userID = db.Column(db.Integer, nullable=False) # ToDo: Ver si hacer esto clave foranea.
    poemID = db.Column(db.Integer, nullable=False) # ToDo: Ver si hacer esto clave foranea.

    # Debuger, mostrar contenido de la tabla.
    def __repr__(self):
        return f"<Mark {self.score} {self.comment} {self.userID} {self.poemID} >"

    #Convertir objeto en JSON
    def to_json(self):
        mark_json = {
            'id': self.id,
            'score': int(self.score),
            'comment': str(self.comment),
            'userID': str(self.userID),
            'poemID': str(self.poemID),
        }
        return mark_json
    
    @staticmethod
    #Convertir JSON a objeto
    def from_json(mark_json):
        id = mark_json.get('id')
        score = mark_json.get('score')
        userID = mark_json.get('userID')
        poemID = mark_json.get('poemID')
        return Mark(id=id,
                    score=score,
                    userID=userID,
                    poemID=poemID,
                    )
