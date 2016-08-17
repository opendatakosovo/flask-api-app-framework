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