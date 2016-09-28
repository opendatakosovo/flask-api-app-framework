from flask import Blueprint, render_template, request, Response
from flask.ext.security import login_required, current_user
from app import org_mongo_utils, content_mongo_utils, user_mongo_utils
from bson.json_util import dumps

mod_organization = Blueprint('organization', __name__, url_prefix='/organization')


@mod_organization.route('/<organization_slug>', methods=['GET'])
def feed(organization_slug):

    organization = org_mongo_utils.get_org_by_slug(organization_slug)

    feed = dumps(content_mongo_utils.get_org_articles(organization_slug))

    return render_template('mod_organization/feed.html', feed=feed, organization=organization, organization_slug=organization_slug)


@mod_organization.route('/<organization_slug>/<category>', methods=['GET'])
def category_feed_org(organization_slug, category):
    ''' Loads the feed page with specific category article.
            '''

    # get the profile object for the given username

    organization = org_mongo_utils.get_org_by_slug(organization_slug)

    feed = dumps(content_mongo_utils.get_articles_one_category_only_org(organization_slug,category))

    return render_template('mod_organization/feed.html', organization=organization, feed=feed, organization_slug=organization_slug)


@mod_organization.route('/<organization_slug>/about', methods=['GET'])
def about(organization_slug):

    # feed = None

    organization = org_mongo_utils.get_org_by_slug(organization_slug)

    articles_no = content_mongo_utils.count_org_articles(organization_slug)

    return render_template('mod_organization/about.html', organization=organization, feed=feed, organization_slug=organization_slug, articles_no=articles_no)


@mod_organization.route('/<organization_slug>/archive', methods=['GET'])
def archive(organization_slug):

    organization = org_mongo_utils.get_org_by_slug(organization_slug)

    category = content_mongo_utils.get_categories()

    articles_by_category_org = content_mongo_utils.count_org_articles_by_category(organization_slug, category)

    return render_template('mod_organization/archive.html', organization=organization, articles_by_category_org=articles_by_category_org)


@mod_organization.route('/<organization_slug>/search', methods=['GET'])
def search(organization_slug):

    organization = org_mongo_utils.get_org_by_slug(organization_slug)

    articles = content_mongo_utils.get_org_articles(organization_slug)

    users = user_mongo_utils.get_users()

    return render_template('mod_organization/search.html', organization=organization, feed=feed, articles=articles, users = users)


@mod_organization.route('/<organization_slug>/settings', methods=['GET'])
def organization_settings(organization_slug):
    # Get the profile info
    organization = org_mongo_utils.get_org_by_slug(organization_slug)

    if request.method == "GET":
        return render_template('mod_organization/account.html', organization=organization, error='')
    elif request.method == "POST":
        user_json = {}
        if request.form['email'] is not None:
            user_json['email'] = request.form['email']
            user_json['name'] = request.form['name']
            user_json['location'] = request.form['location']
            user_json['telephone'] = request.form['telephone']
            user_json['mobile'] = request.form['mobile']
            user_json['about_us'] = request.form['about_me']
            org_mongo_utils.update({'username': current_user.username}, user_json)
        return render_template('mod_organization/account.html', organization=organization, error="Succesfully updated organization profile.")


@mod_organization.route('/<organization_slug>/<action>', methods=['POST'])
def follow(organization_slug, action):
    '''
    TODO:
        1. Get POST reuqest body JSON
        2. Get the username of the follower.
        3. Implement org_mongo_utils.add_follower()
        4. Call org_mongo_utils.add_follower()
        5. Check if it adds the follower username in the document.
        6. Implement org_mongo_utils.remove_follower()
    '''
    follower_username = current_user.username
    org_mongo_utils.add_follower(follower_username, organization_slug, action)
    resp = Response(status=200)
    return resp


@mod_organization.route('/<organization_slug>/memberships', methods=['GET'])
def memberships(organization_slug):

    # profile = user_mongo_utils.get_user_by_username(username)
    return render_template('mod_organization/memberships.html')
