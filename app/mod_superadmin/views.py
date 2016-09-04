from flask import Blueprint, render_template
from app import user_mongo_utils, bcrypt
from flask import request
from flask import Response
import json
from slugify import slugify

mod_superadmin = Blueprint('superadmin', __name__, url_prefix='/sadmin')


@mod_superadmin.route('/', methods=['GET'])
def index():
    return render_template('mod_superadmin/index.html')

@mod_superadmin.route('/users', methods=['GET'])
def users():

    users = user_mongo_utils.get_users()
    return render_template('mod_superadmin/users.html', users=users)


@mod_superadmin.route('/add_users', methods=['GET','POST'])
def add_users():
    if request.method=='GET':
        return render_template('mod_superadmin/add_users.html')
    elif request.method=='POST':
        name = request.form['name']
        lastname = request.form['lastname']
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form['confirm_password']
        role = request.form['role']
        if password == confirm_password:
            user_json = {
                "name": name,
                "lastname": lastname,
                "email": email,
                "password": bcrypt.generate_password_hash(password, rounds=12),
                "active": True,
                "user_slug": slugify(name + ' ' + lastname),
                "roles": [user_mongo_utils.get_role_id(role)],
                "role": role,
                "organizations": ['kreotive']
            }
            # TODO: Regiser user
            user_mongo_utils.add_user(user_json)

        return render_template('mod_superadmin/add_users.html')
