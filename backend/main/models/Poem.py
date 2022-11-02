from .. import db
from datetime import datetime

class Poem(db.Model):

    # Generamos las columnas de Usuario
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    #userID = db.Column(db.Integer, nullable=False) # ToDo: Ver si hacer esto clave foranea.
    body = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())

    # Crear Clave Foranea
    userID = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    # Relación
    user = db.relationship("User", back_populates="poems", uselist=False, single_parent=True)
    marks = db.relationship("Mark", back_populates="poem", cascade="all, delete-orphan")

    # Debuger, mostrar contenido de la tabla.
    def __repr__(self):
        return f"<Poem {self.id} {self.title} {self.userID} {self.body} {self.created_at}>"

    #Convertir objeto en JSON. Visual para no usuarios
    def to_json(self):
        poem_json = {
            'id': int(self.id),
            'title': str(self.title),
            'user': self.user.to_json(),
            'body': str(self.body),
            'marksAvrg': self.__averageMarks(),
            #'marks': [mark.to_json() for mark in self.marks]
            'created_at': str(self.created_at)
        }
        return poem_json

    #Convertir objeto en JSON. Visual para usuarios
    def to_json_user(self):
        poem_json = {
            'id': int(self.id),
            'title': str(self.title),
            'user': self.user.to_json_user(),
            'body': str(self.body),
            'marksAvrg': self.__averageMarks(),
            #'marks': [mark.to_json() for mark in self.marks]
            'created_at': str(self.created_at)
        }
        return poem_json

    #Convertir objeto en JSON. Visual para admin
    def to_json_admin(self):
        poem_json = {
            'id': int(self.id),
            'title': str(self.title),
            'user': self.user.to_json_admin(),
            'body': str(self.body),
            'marksAvrg': self.__averageMarks(),
            #'marks': [mark.to_json() for mark in self.marks]
            'created_at': str(self.created_at)
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
                    body=body
                    #created_at=created_at
                    )

    # Funciones de Utilidad
    def __averageMarks(self):
        """
        Devuelve el Promedio de las calificaciones.
        """
        #Si marks es vacio devuelve cero.
        if len(self.marks) == 0:
            return 0
        else:
            score = 0
            total = 0
            for mark in self.marks:
                score += mark.score
                total += 1
            value = round(score/total, 2)
            return value
