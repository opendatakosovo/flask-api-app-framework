from flask import Blueprint, render_template

mod_main = Blueprint('main', __name__)


@mod_main.route('/register', methods=['GET'])
def sign():
    ''' Renders the App index page.
    :return:
    '''
    return render_template('mod_main/sign_up.html')

@mod_main.route('/', methods=['GET'])
@mod_main.route('/feed', methods=['GET'])
def feed():
    ''' Renders the App index page.
    :return:
    '''
    return render_template('mod_feed/feed.html')

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