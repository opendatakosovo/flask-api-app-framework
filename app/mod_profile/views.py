from flask import Blueprint, render_template
from app import profile_mongo_utils


mod_profile = Blueprint('profile', __name__, url_prefix='/profile')


@mod_profile.route('/<slug>/archive', methods=['GET'])
def archive(slug):
    ''' Loads the article archive page.
    '''

    # get the profile object for the given slug
    profile = profile_mongo_utils.get_profile(slug)

    # TODO: Figure out how we get categorized content.

    return render_template('mod_profile/archive.html', profile=profile)


@mod_profile.route('/<slug>/about', methods=['GET'])
def about(slug):
    ''' Loads the about page.
    '''

    # get the profile object for the given slug
    profile = profile_mongo_utils.get_profile(slug)

    return render_template('mod_profile/about.html', profile=profile)


@mod_profile.route('/<slug>', methods=['GET'])
def feed(slug):
    ''' Loads the feed page.
    '''

    # get the profile object for the given slug
    profile = profile_mongo_utils.get_profile(slug)

    # TODO: load feed content for given slug
    feed = None
    # feed = content_mongo_utils.get_feed(slug)

    return render_template('mod_profile/feed.html', profile=profile, feed=feed)


@mod_profile.route('/<slug>/follow', methods=['POST'])
def follow():
    '''
    TODO:
        1. Get POST reuqest body JSON
        2. Get the SLUG of the follower.
        3. Implement profile_mongo_utils.add_follower()
        4. Call profile_mongo_utils.add_follower()
        5. Check if it adds the follower slug in the document.
        6. Implement profile_mongo_utils.remove_follower()
    '''

    pass
