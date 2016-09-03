import datetime
from bson.objectid import ObjectId


class ContentMongoUtils(object):

    def __init__(self, mongo):
        self.mongo = mongo
        self.content_collection = 'content'

    def add_article(self, content):
        self.mongo.db[self.content_collection] \
                .insert(content)
        return True

    def get_articles(self):
    	articles = self.mongo.db[self.content_collection] \
                .find()
        return articles

    def get_single_article(self, slug):
    	articles = self.mongo.db[self.content_collection] \
                .find_one({"slug":slug})
        return articles

    def get_authors_articles(self, author_id):
    	articles = self.mongo.db[self.content_collection] \
                .find({"user":author_id})
        return articles