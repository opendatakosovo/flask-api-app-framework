from flask import Blueprint, render_template
from app import profile_mongo_utils


mod_profile = Blueprint('profile', __name__, url_prefix='/profile')


@mod_profile.route('/<slug>/archive', methods=['GET'])
def archive(slug):

    # get the profile object for the given slug
    profile = profile_mongo_utils.get_profile(slug)

    # TODO: Figure out how we get categorized content.

    return render_template('mod_profile/archive.html', profile=profile)


@mod_profile.route('/<slug>/about', methods=['GET'])
def about(slug):

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
