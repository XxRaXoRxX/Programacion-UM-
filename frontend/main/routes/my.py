from flask import Blueprint, redirect, url_for

#Crear Blueprint
my = Blueprint('main', __name__, url_prefix='/my')

# Ver información del usuario
@my.route('/')
def index():
    return redirect(url_for('user_info.html'))

# Ver poemas del usuario
@my.route('/poems')
def index():
    return redirect(url_for('poems.html'))

# Editar usuario
@my.route('/edit')
def index():
    return redirect(url_for('user_config.html'))

# Eliminar cuenta del usuario
@my.route('/delete')
def index():
    return redirect(url_for('delete_account.html'))

# Cambiar contraseña del usuario
@my.route('/password')
def index():
    return redirect(url_for('change_password.html'))

