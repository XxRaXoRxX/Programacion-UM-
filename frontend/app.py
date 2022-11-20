import os
from main import create_app

# Creamos la app en flask que se encuentra dentro del "main/__init__.py"
app = create_app()

# Hacer push sobre el contexto de la app.
app.app_context().push()

#Esto permite acceder a las propiedades de la app
if __name__ == "__main__":
    app.run(debug = True, port = os.getenv("PORT"))