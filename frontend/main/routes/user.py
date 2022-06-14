from flask import Blueprint, redirect, url_for

#Crear Blueprint
user = Blueprint('main', __name__, url_prefix='/')

# Ver información de usuario por id.
@user.route('/view/<int:id>')
def view(id):
    return redirect(url_for('user_info.html'))
