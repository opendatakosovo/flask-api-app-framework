import datetime
from bson.objectid import ObjectId
from bson.json_util import json


class BookmarksMongoUtils(object):
    def __init__(self, mongo):
        self.mongo = mongo
        self.bookmarks_collection = 'bookmarks'
        self.content_collection = 'content'

    def bookmark_article(self, username, slug):
        self.mongo.db[self.bookmarks_collection] \
            .insert_one({"username": username, "slug": slug})
        return True

    def get_bookmark_article(self, username, slug):
        bookmark = self.mongo.db[self.bookmarks_collection] \
            .find_one({"username": username, "slug": slug})
        if bookmark:
            return True
        else:
            return False

    def remove_bookmark(self, username, slug):
        remove_bookmark = self.mongo.db[self.bookmarks_collection] \
            .remove({"username": username, "slug": slug})
        return remove_bookmark

    def get_bookmark_list(self, username):

        bookmarks = self.mongo.db[self.bookmarks_collection] \
            .find({"username": username})
        return bookmarks

    def get_article_title(self,slug):

        article = self.mongo.db[self.content_collection] \
        .find_one({"slug":slug})

        return article

