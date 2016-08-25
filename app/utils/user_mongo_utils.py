class UserMongoUtils(object):
    def __init__(self, mongo):
        self.mongo = mongo
        self.collection_name = 'user'

    def add_user(self, user):
        self.mongo.db[self.collection_name] \
            .insert(user)

        return True

