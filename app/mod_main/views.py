from flask import Blueprint, render_template
from app import content_mongo_utils
from bson.json_util import dumps

mod_main = Blueprint('main', __name__)


@mod_main.route('/', methods=['GET'])
def feed():
    ''' Renders the App index page.
    :return:
    '''
    articles = dumps(content_mongo_utils.get_articles())

    return render_template('mod_feed/feed.html', articles=articles)


@mod_main.route('/write-article', methods=['GET'])
def write():
    ''' Renders the App index page.
    :return:
    '''
    return render_template('mod_article/write_article.html')


@mod_main.route('/manage', methods=['GET'])
def manage():
    ''' Renders the App index page.
    :return:
    '''
    return render_template('mod_article/article_management.html')