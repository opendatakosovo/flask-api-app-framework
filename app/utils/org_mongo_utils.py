class OrgMongoUtils(object):

    def __init__(self, mongo):
        self.mongo = mongo
        self.org_collection = 'organizations'

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
