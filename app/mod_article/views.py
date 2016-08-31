from flask import Blueprint, render_template
from app import user_mongo_utils
from flask import request
from flask import Response
import json


mod_article= Blueprint('article', __name__, url_prefix='/article')


@mod_article.route('/<slug>', methods=['GET'])
def article(slug):

    return render_template('mod_article/article_single.html')

@mod_article.route('/<user_id>/<org_id_id>')
def articles(user_id,org_id):
	return render_template('mod_article/article_management.html')
@mod_article.route('/new', , methods=['GET','POST'])
def new_article(slug):

    return render_template('mod_article/write_article.html')

