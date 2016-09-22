from flask import Blueprint, render_template, request, Response, redirect, url_for
from app import content_mongo_utils, profile_mongo_utils, org_mongo_utils, user_mongo_utils
from flask.ext.security import current_user
from slugify import slugify
from datetime import datetime
from bson.json_util import dumps


mod_article = Blueprint('article', __name__, url_prefix='/article')


@mod_article.route('/<slug>', methods=['GET'])
def article(slug):
    # TODO: Restrict access to only authenticated users if the article has "visible" set to False
    article = content_mongo_utils.get_single_article(slug)

    profile = None
    organization = None
    if article['author']['type'] == 'individual':
        profile = profile_mongo_utils.get_profile(article['author']['slug'])
    elif article['author']['type'] == 'organization':
        organization = org_mongo_utils.get_org_by_slug(article['author']['org_slug'])
    return render_template('mod_article/article_single.html', article=article, profile=profile, organization=organization)


@mod_article.route('/<user_id>/<org_id>')
def organization_author_articles(user_id, org_id):
    # TODO: Restrict access to only authenticated users
    return render_template('mod_article/article_management.html')


@mod_article.route('/<org_id>')
def organization_articles(org_id):
    # TODO: Restrict access to only authenticated users
    return render_template('mod_article/article_management.html')


@mod_article.route('/user/<username>')
def authors_articles(username):
    # TODO: Restrict access to only authenticated users
    articles = content_mongo_utils.get_authors_articles(username)
    return render_template('mod_article/article_management.html', articles=articles)


@mod_article.route('/my-articles/<string:article_action>')
def my_articles(article_action):
    message = None
    if article_action == "save":
        message = "Your article has been saved, but not published."
    elif article_action == "publish":
        message = "Your article has been published."
    elif article_action == "show":
        message = "Showing your latest articles"
    elif article_action == 'delete':
        message = "Article/s deleted."
    # TODO: Restrict access to only authenticated users
    articles = content_mongo_utils.get_authors_articles(current_user.username)
    return render_template('mod_article/article_management.html', articles=articles, article_action=article_action,
                           message=message)


@mod_article.route('/<string:author_type>/<string:name>/<string:username>/new', methods=["POST", "GET"])
def new_article(author_type, name, username):
    if request.method == "GET":
        return render_template('mod_article/write_article.html')
    elif request.method == "POST":
        form = request.form
        if author_type == "individual":
            new_article_from_author(form, name, username)
            return redirect(url_for('article.my_articles', article_action='show'))
        elif author_type == "organization":
            new_article_from_org(form, name, username)
            return redirect(url_for('article.my_articles', article_action='show'))
    return redirect(url_for('article.my_articles', article_action='show'))

def new_article_from_author(form, name, username):
    action = form['action']
    content = form['content']
    category = form['category']
    title = form['title']
    type = form['type']
    publish_article = True
    if action == "save":
        publish_article = False
    elif action == "cancel":
        return redirect(url_for('article.my_articles', article_action='show'))
    content_mongo_utils.add_article({
        "content": content,
        "visible": publish_article,
        "category": category,
        "title": title,
        "slug": slugify(title),
        "type": type,
        "username": current_user.username,
        "published": publish_article,
        "published_date": datetime.now(),
        "author": {
            "type": "individual",
            "slug": username,
            "name": name,
            "lastname": current_user.lastname
        }
    })
    return redirect(url_for('article.my_articles', article_action='save'))


def new_article_from_org(form, name, username):
    action = form['action']
    content = form['content']
    category = form['category']
    title = form['title']
    type = form['type']
    publish_article = True
    if action == "save":
        publish_article = False
    elif action == "cancel":
        return redirect(url_for('article.my_articles', article_action='show'))
    content_mongo_utils.add_article({
        "content": content,
        "visible": publish_article,
        "category": category,
        "title": title,
        "slug": slugify(title),
        "type": type,
        "username": current_user.username,
        "published": publish_article,
        "published_date": datetime.now(),
        "author": {
            "type": "organization",
            "org_slug": username ,
            "org_name": name,
            "name": current_user.name,
            "lastname": current_user.lastname
        }
    })
    return redirect(url_for('article.my_articles', article_action='save'))

@mod_article.route('/visibility/<article_id>/<visible>', methods=["POST", "GET"])
def edit_article_visibility(article_id, visible):
    update = content_mongo_utils.change_article_visibility(article_id, visible)
    return redirect(url_for('article.my_articles', article_action='show'))


@mod_article.route('/articles/<int:skip_posts_number>/<int:posts_per_page>', methods=['POST'])
def paginated_articles(skip_posts_number, posts_per_page):
    # TODO: Restrict access to only authenticated users
    articles = dumps(content_mongo_utils.get_paginated_articles(skip_posts_number, posts_per_page))

    return Response(response=articles)


@mod_article.route('/delete/<article_id>', methods=['POST', 'GET'])
def delete_article(article_id):
    # TODO: Restrict access to only authenticated users
    delete_article = content_mongo_utils.delete_article(article_id)
    return redirect(url_for('article.my_articles', article_action='delete'))
