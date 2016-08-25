from flask import Blueprint, render_template
from app import profile_mongo_utils

mod_user= Blueprint('user', __name__, url_prefix='/user')

@mod_user.route('/account', methods=['GET'])
def account():
    return render_template('mod_user/account.html')