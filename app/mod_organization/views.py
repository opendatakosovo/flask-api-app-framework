from flask import Blueprint, render_template
from app import content_mongo_utils
from bson.json_util import dumps
from app import user_mongo_utils, content_mongo_utils, profile_mongo_utils

mod_organization = Blueprint('organization', __name__, url_prefix='/organization')

@mod_organization.route('/', methods=['GET'])
def feed():

    # organization= user_mongo_utils.get_user_by_slug(organization_slug)


    return render_template('mod_organization/org_feed.html',feed=feed)


@mod_organization.route('/about', methods=['GET'])
def about():

    # organization = user_mongo_utils.get_user_by_slug(organization_slug)

    return render_template('mod_organization/org_about.html',feed=feed)


@mod_organization.route('/archive', methods=['GET'])
def archive():

    # organization = user_mongo_utils.get_user_by_slug(organization_slug)

    return render_template('mod_organization/org_archive.html',feed=feed)

@mod_organization.route('/search', methods=['GET'])
def search():
    #
    # organization = user_mongo_utils.get_user_by_slug(organization_slug)

    return render_template('mod_organization/org_search.html',feed=feed)
