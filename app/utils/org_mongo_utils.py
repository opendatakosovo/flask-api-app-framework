class OrgMongoUtils(object):

    def __init__(self, mongo):
        self.mongo = mongo
        self.org_collection = 'organizations'
        self.users_collection = 'users'

    def add_org(self, org):
        """ Add user to the database.
         :param org: JSON object containing the user information
         :rtype: Boolean
        """
        self.mongo.db[self.org_collection] \
            .insert(org)
        return True

    def get_org_by_slug(self, org_slug):
        """ Get an organization by slug.
         :param org_slug: Slug of the organization
         :rtype: MongoDB Cursor
        """
        org_cursor = self.mongo.db[self.org_collection] \
            .find_one({"org_slug": org_slug})
        return org_cursor

    def get_organizations(self):
        """ Get all organizations.
         :rtype: MongoDB Cursor
        """
        org_cursor = self.mongo.db[self.org_collection] \
            .find()
        return org_cursor

    def find_org(self,keyword):

        find_org_result = self.mongo.db[self.org_collection] \
            .find({'$text': {'$search': keyword}})
        return find_org_result

    def add_follower(self, follower_username, organization_slug, action):
        if action == 'follow':
            added_follower_to_current_user = self.mongo.db[self.org_collection].update(
                {"org_slug": organization_slug},
                {"$addToSet": {"followers": follower_username}}
            )

            added_followee_to_the_user_ = self.mongo.db[self.users_collection].update(
                {"username": follower_username},
                {"$addToSet": {"org_following": organization_slug}}
            )

            if added_followee_to_the_user_['updatedExisting'] and added_follower_to_current_user['updatedExisting']:
                return True
            else:
                return False
        elif action == 'unfollow':

            added_follower_to_current_user = self.mongo.db[self.org_collection].update(
                {"org_slug": organization_slug},
                {"$pull": {"organizations.followers": follower_username}}
            )

            added_followee_to_the_user_ = self.mongo.db[self.users_collection].update(
                {"username": follower_username},
                {"$pull": {"org_following": organization_slug}}
            )

            if added_followee_to_the_user_['updatedExisting'] and added_follower_to_current_user['updatedExisting']:
                return True
            else:
                return False