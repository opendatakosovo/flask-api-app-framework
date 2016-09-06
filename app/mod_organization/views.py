from flask import Blueprint, render_template
from app import content_mongo_utils
from bson.json_util import dumps
from app import user_mongo_utils, content_mongo_utils, profile_mongo_utils

mod_organization = Blueprint('organization', __name__, url_prefix='/organization')

@mod_organization.route('/<organization_slug>', methods=['GET'])
def feed(organization_slug):

    organization= user_mongo_utils.get_user_by_slug(organization_slug)


    return render_template('mod_organization/org_feed.html', organization=organization, feed=feed)


@mod_organization.route('/<organization_slug>/about', methods=['GET'])
def about(organization_slug):

    organization = user_mongo_utils.get_user_by_slug(organization_slug)

    return render_template('mod_organization/org_about.html', organization=organization, feed=feed)


@mod_organization.route('/<organization_slug>/archive', methods=['GET'])
def archive(organization_slug):

    organization = user_mongo_utils.get_user_by_slug(organization_slug)

    return render_template('mod_organization/org_archive.html', organization=organization, feed=feed)
