from .. import db

class Mark(db.Model):

    # Generamos las columnas de Usuario
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(100), nullable=True)

    # Crear Clave Foranea 
    userID = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    poemID = db.Column(db.Integer, db.ForeignKey("poem.id"), nullable=False)

    # Relación
    user = db.relationship("User", back_populates="marks", uselist=False, single_parent=True)
    poem = db.relationship("Poem", back_populates="marks", uselist=False, single_parent=True)

    # Debuger, mostrar contenido de la tabla.
    def __repr__(self):
        return f"<Mark {self.score} {self.comment} {self.userID} {self.poemID} >"

    #Convertir objeto en JSON. Visual para no usuarios
    def to_json(self):
        mark_json = {
            'id': self.id,
            'score': int(self.score),
            'comment': str(self.comment),
            'user': self.user.to_json(),
            'poem': self.poem.to_json()
        }
        return mark_json

    #Convertir objeto en JSON. Visual para usuarios
    def to_json_user(self):
        mark_json = {
            'id': self.id,
            'score': int(self.score),
            'comment': str(self.comment),
            'user': self.user.to_json_user(),
            'poem': self.poem.to_json_user()
        }
        return mark_json

    #Convertir objeto en JSON. Visual para admin
    def to_json_admin(self):
        mark_json = {
            'id': self.id,
            'score': int(self.score),
            'comment': str(self.comment),
            'user': self.user.to_json_admin(),
            'poem': self.poem.to_json_admin()
        }
        return mark_json
    
    @staticmethod
    #Convertir JSON a objeto
    def from_json(mark_json):
        id = mark_json.get('id')
        score = mark_json.get('score')
        comment = mark_json.get('comment')
        userID = mark_json.get('userID')
        poemID = mark_json.get('poemID')
        return Mark(id=id,
                    score=score,
                    comment=comment,
                    userID=userID,
                    poemID=poemID
                    )
