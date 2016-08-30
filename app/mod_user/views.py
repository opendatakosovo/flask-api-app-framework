from flask import Blueprint, render_template
from app import user_mongo_utils
from flask import request
from flask import Response
import json


mod_user= Blueprint('user', __name__, url_prefix='/user')


@mod_user.route('/<slug>/account', methods=['GET'])
def account(slug):

        return render_template('mod_user/account.html')


@mod_user.route('/<slug>/articles', methods=['GET'])
def articles(slug):

        return render_template('mod_user/articles.html')


@mod_user.route('/<slug>/memberships', methods=['GET'])
def memberships(slug):

        return render_template('mod_user/memberships.html')


@mod_user.route('/<slug>/account/save', methods=['POST'])
def save(slug):
    user_json = {
        "name": request.form["name"],
        "email": request.form["email"],
        "location": request.form["location"],
        "telephone": request.form["telephone"],
        "mobile": request.form["mobile"],
        "about": request.form["about"]
    }

    user_mongo_utils.add_user(user_json)
    resp = Response(status=200)
    return resp

