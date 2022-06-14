from flask import Blueprint, redirect, url_for, render_template

#Crear Blueprint
my = Blueprint('my', __name__, url_prefix='/my')

# Ver información del usuario
@my.route('/')
def index():
    return render_template('user_info.html')

# Ver poemas del usuario
@my.route('/poems')
def poems():
    return render_template('poems.html')

# Editar usuario
@my.route('/edit')
def edit():
    return render_template('user_config.html')

# Eliminar cuenta del usuario
@my.route('/delete')
def delete():
    return render_template('delete_account.html')

# Cambiar contraseña del usuario
@my.route('/password')
def password():
    return render_template('change_password.html')

