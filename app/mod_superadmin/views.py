from flask import Blueprint, render_template
from app import user_mongo_utils
from flask import request
from flask import Response
import json


mod_superadmin= Blueprint('superadmin', __name__, url_prefix='/sadmin')


@mod_superadmin.route('/', methods=['GET'])
def index():

        return render_template('mod_superadmin/index.html')


