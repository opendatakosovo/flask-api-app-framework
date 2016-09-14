from flask import Blueprint, render_template
from flask.ext.security import login_required
from app import org_mongo_utils

mod_organization = Blueprint('organization', __name__, url_prefix='/organization')


@mod_organization.route('/<organization_slug>', methods=['GET'])
def feed(organization_slug):

    feed = None

    organization= org_mongo_utils.get_org_by_slug(organization_slug)

    return render_template('mod_organization/feed.html', organization=organization, feed=feed)

@mod_organization.route('/<organization_slug>/about', methods=['GET'])
def about(organization_slug):

    feed = None

    organization = org_mongo_utils.get_org_by_slug(organization_slug)

    return render_template('mod_organization/about.html', organization=organization, feed=feed)


@mod_organization.route('/<organization_slug>/archive', methods=['GET'])
def archive(organization_slug):

    feed = None

    organization = org_mongo_utils.get_org_by_slug(organization_slug)

    return render_template('mod_organization/archive.html', organization=organization, feed=feed)

@mod_organization.route('/<organization_slug>/search', methods=['GET'])
def search(organization_slug):

    feed = None

    organization = org_mongo_utils.get_org_by_slug(organization_slug)

    return render_template('mod_organization/search.html', organization=organization, feed=feed)
