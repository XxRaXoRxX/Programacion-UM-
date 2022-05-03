from .. import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):

    # Generamos las columnas de Usuario
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    rol = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(100), unique = True, index = True, nullable=False) #unique sirve para que no haya duplicados en la db.

    # Relaciones
    poems = db.relationship("Poem", back_populates="user", cascade="all, delete-orphan")
    marks = db.relationship("Mark", back_populates="user", cascade="all, delete-orphan")

    # Debuger, mostrar contenido de la tabla.
    def __repr__(self):
        return f"<Professor: {self.name} {self.password} {self.rol} {self.email} >"

    @property #En caso de lectura, le de un error.
    def plain_password(self):
        raise AttributeError('Password cant be read')

    @plain_password.setter #En caso de escritura que genere el hash y lo ingrese a contraseña.
    def plain_password(self, password):
        self.password = generate_password_hash(password)

    #Método que compara una contraseña en texto plano con el hash guardado en la base de datos
    def validate_pass(self,password):
        return check_password_hash(self.password, password)

    #Convertir objeto en JSON. Visual para usuarios
    def to_json_user(self):
        user_json = {
            'id': self.id,
            'name': str(self.name),
            'poemsAmount': len(self.poems),
            'ratingAmount': len(self.marks)
            #'poems': [poem.to_json() for poem in self.poems],
            #'marks': [mark.to_json() for mark in self.marks]
            #'password': str(self.password)
            #'rol': str(self.rol),
            #'email': str(self.email),
        }
        return user_json

    #Convertir objeto en JSON. Visual para admin
    def to_json_admin(self):
        user_json = {
            'id': self.id,
            'name': str(self.name),
            'poemsAmount': len(self.poems),
            'ratingAmount': len(self.marks),
            'rol': str(self.rol),
            'email': str(self.email)
        }
        return user_json

    #Convertir objeto en JSON. Visual para no usuarios
    def to_json(self):
        user_json = {
            #'id': self.id,
            'name': str(self.name),
            #'poemsAmount': len(self.poems),
            'ratingAmount': len(self.marks)
        }
        return user_json
    
    @staticmethod
    #Convertir JSON a objeto
    def from_json(user_json):
        id = user_json.get('id')
        name = user_json.get('name')
        password = user_json.get('password')
        rol = user_json.get('rol')
        email = user_json.get('email')
        return User(id=id,
                    name=name,
                    plain_password=password,
                    rol=rol,
                    email=email
                    )

