from flask import Blueprint, render_template, request, Response, redirect, url_for
from app import content_mongo_utils
from flask.ext.security import current_user
from slugify import slugify
from datetime import datetime
from bson.json_util import dumps

mod_article = Blueprint('article', __name__, url_prefix='/article')


@mod_article.route('/<slug>', methods=['GET'])
def article(slug):
    # TODO: Restrict access to only authenticated users if the article has "visible" set to False
    article = content_mongo_utils.get_single_article(slug)
    return render_template('mod_article/article_single.html', article=article)


@mod_article.route('/<user_id>/<org_id>')
def organization_author_articles(user_id, org_id):
    # TODO: Restrict access to only authenticated users
    return render_template('mod_article/article_management.html')


@mod_article.route('/<org_id>')
def organization_articles(org_id):
    # TODO: Restrict access to only authenticated users
    return render_template('mod_article/article_management.html')


@mod_article.route('/user/<user_id>')
def authors_articles(user_id):
    # TODO: Restrict access to only authenticated users
    articles = content_mongo_utils.get_authors_articles(user_id)
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
    # TODO: Restrict access to only authenticated users
    articles = content_mongo_utils.get_authors_articles(current_user.id)
    return render_template('mod_article/article_management.html', articles=articles, article_action=article_action,
                           message=message)


@mod_article.route('/new', methods=["POST", "GET"])
def new_article():
    # TODO: Restrict access to only authenticated users
    if request.method == "GET":
        return render_template('mod_article/write_article.html')
    elif request.method == "POST":
        action = request.form['action']
        content = request.form['content']
        category = request.form['category']
        title = request.form['title']
        if action == "save":
            content_mongo_utils.add_article(
                {"content": content, "visible": True, "category": category, "title": title, "slug": slugify(title),
                 "user": current_user.id, "published": False, "published_date": datetime.now(),
                 "author_slug": current_user.user_slug, "author_name": current_user.name,
                 "author_lastname": current_user.lastname})
            return redirect(url_for('article.my_articles', article_action='save'))
        elif action == "publish":
            content_mongo_utils.add_article(
                {"content": content, "visible": True, "category": category, "title": title, "slug": slugify(title),
                 "user": current_user.id, "published": True, "published_date": datetime.now(),
                 "author_slug": current_user.user_slug, "author_name": current_user.name,
                 "author_lastname": current_user.lastname})
            return redirect(url_for('article.my_articles', article_action='publish'))
        elif action == "cancel":
            return redirect(url_for('article.my_articles'))
        return render_template('mod_article/write_article.html')


@mod_article.route('/edit-article-visibility/<article_id>/<visibility>', methods=["POST", "GET"])
def edit_article_visibility(article_id, visibility):
    content_mongo_utils.change_article_visibility(article_id, visibility)
    return redirect(url_for('article.my_articles', article_action='show'))


@mod_article.route('/articles/<int:skip_posts_number>/<int:posts_per_page>', methods=['POST'])
def paginated_articles(skip_posts_number, posts_per_page):
    # TODO: Restrict access to only authenticated users
    articles = dumps(content_mongo_utils.get_paginated_articles(skip_posts_number, posts_per_page))
    return Response(response=articles)

