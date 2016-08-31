from flask import Blueprint, render_template, url_for, redirect, flash, jsonify
from flask.ext.security import login_user , logout_user , current_user , login_required
from app import user_mongo_utils, bcrypt
from flask import request
from flask import Response
import json
from app.utils.user_mongo_utils import Roles

mod_auth= Blueprint('auth', __name__, url_prefix='/auth')


@mod_auth.route('/sign-up', methods=["POST","GET"])
def sign_up():

    if request.method == "GET":
        return render_template('mod_auth/sign_up.html')
    elif request.method == "POST":
        name= request.form['name']
        lastname=request.form['lastname']
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form['confirm_password']

        if password == confirm_password:
            user_json = {
                "name":name,
                "lastname": lastname,
                "email": email,
                "password": bcrypt.generate_password_hash(password, rounds=12),
                "active": True,
                "roles": [user_mongo_utils.get_role_id('individual')],
                "organizations" : ['kreotive']
            }
            #TODO: Regiser user
            user_mongo_utils.add_user(user_json)
            flash('User successfully registered')

            #TODO: login user
            return redirect(url_for('main.feed'))

        return render_template('mod_auth/sign_up.html', error="user:" + email + "password" + password)


@mod_auth.route('/login', methods=["POST","GET"])
def login():
    error =""
    if request.method == "GET":
        return render_template('mod_auth/log_in.html')
    elif request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        user_input = user_mongo_utils.get_user(email=email)
        if user_input is None:
            error = 'Please write both username and password', 'error'
            return render_template('mod_auth/log_in.html', error=error)
        elif user_input != None :
            password_check = bcrypt.check_password_hash(user_input.password, password)
            email_check = True if user_input.email==email else False
            if  not email_check:
                error = 'Wrong email'
                return render_template('mod_auth/log_in.html', error=error)
            elif not password_check :
                error = 'Wrong password'
                return render_template('mod_auth/log_in.html', error=error)
            elif password_check and email_check:
                login_user(user_input)
                # print current_user.is_authenticated()
                return redirect(url_for('main.feed'))

@mod_auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.feed'))