from flask import Blueprint, render_template, request, Response
from app import profile_mongo_utils, content_mongo_utils, user_mongo_utils
from bson.json_util import dumps

mod_profile = Blueprint('profile', __name__, url_prefix='/profile')


@mod_profile.route('/<profile_slug>/archive', methods=['GET'])
def archive(profile_slug):
    ''' Loads the article archive page.
    '''

    # get the profile object for the given slug
    profile = user_mongo_utils.get_user_by_slug(profile_slug)

    # TODO: load feed content for given slug
    feed = content_mongo_utils.get_authors_articles(profile.id)

    return render_template('mod_profile/archive.html', profile=profile, feed=feed)


@mod_profile.route('/<profile_slug>/about', methods=['GET'])
def about(profile_slug):
    ''' Loads the about page.
    '''

    # get the profile object for the given slug
    profile = user_mongo_utils.get_user_by_slug(profile_slug)

    return render_template('mod_profile/about.html', profile=profile)


@mod_profile.route('/<profile_slug>', methods=['GET'])
def feed(profile_slug):
    ''' Loads the feed page.
    '''

    # get the profile object for the given slug
    profile = user_mongo_utils.get_user_by_slug(profile_slug)

    # TODO: load feed content for given slug

    feed = dumps(content_mongo_utils.get_authors_paginated_articles(profile.id, 0, 6))

    return render_template('mod_profile/feed.html', profile=profile, feed=feed)


@mod_profile.route('/<profile_slug>/follow', methods=['POST'])
def follow(profile_slug):
    '''
    TODO:
        1. Get POST reuqest body JSON
        2. Get the SLUG of the follower.
        3. Implement profile_mongo_utils.add_follower()
        4. Call profile_mongo_utils.add_follower()
        5. Check if it adds the follower slug in the document.
        6. Implement profile_mongo_utils.remove_follower()
    '''

    follower_slug = request.json["follower"]
    profile_mongo_utils.add_follower(profile_slug, follower_slug)
    resp = Response(status=200)

    return resp

@mod_profile.route('/articles/<profile_slug>/<int:skip_posts_number>/<int:posts_per_page>', methods=['POST'])
def paginated_author_articles(profile_slug,skip_posts_number, posts_per_page):
    # TODO: Restrict access to only authenticated users
     # get the profile object for the given slug
    profile = user_mongo_utils.get_user_by_slug(profile_slug)
    articles = dumps(content_mongo_utils.get_authors_paginated_articles(profile.id, skip_posts_number, posts_per_page))
    return Response(response=articles)
