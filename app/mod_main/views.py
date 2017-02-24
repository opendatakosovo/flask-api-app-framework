from flask import Blueprint, render_template
from app import content_mongo_utils
from bson.json_util import dumps

mod_main = Blueprint('main', __name__)


@mod_main.route('/', methods=['GET'])
def feed():
    ''' Renders the App index page.
    :return:
    '''
    articles = dumps(content_mongo_utils.get_paginated_articles(0,6))
    return render_template('mod_feed/feed.html', articles=articles)
