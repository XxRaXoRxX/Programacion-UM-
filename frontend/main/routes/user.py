from flask import Blueprint, redirect, url_for, render_template

#Crear Blueprint
user = Blueprint('user', __name__, url_prefix='/user')

# Ver información de usuario por id.
@user.route('/view/<int:id>')
def view(id):
    return render_template('user_info.html')
