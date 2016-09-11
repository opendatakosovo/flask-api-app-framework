from flask import Blueprint, render_template, url_for
from app import content_mongo_utils, org_mongo_utils, user_mongo_utils
from bson.json_util import dumps

mod_main = Blueprint('main', __name__)


@mod_main.route('/', methods=['GET'])
def feed():
    ''' Renders the App index page.
    :return:
    '''
    articles_cursor = content_mongo_utils.get_paginated_articles(0, 6)
    articles = dumps(articles_cursor)
    # TODO: Create a macro for jinja where you can get avatar link by username
    return render_template('mod_feed/feed.html', articles=articles)


@mod_main.route('/organizations/search', methods=['GET'])
def search_organizations():
    ''' Renders the Search organizations page.
    :return:
    '''
    organizations = org_mongo_utils.get_organizations()
    return render_template('mod_feed/search.html', organizations=organizations)

@mod_main.route('/articles/search', methods=['GET'])
def search_articles():
    ''' Renders the Search Articles page.
    :return:
    '''
    articles = content_mongo_utils.get_articles()
    return render_template('mod_feed/search_articles.html', articles=articles)

@mod_main.route('/people/search', methods=['GET'])
def search_people():
    ''' Renders the Search people page.
    :return:
    '''
    users = user_mongo_utils.get_users()
    return render_template('mod_feed/search_people.html', users=users)