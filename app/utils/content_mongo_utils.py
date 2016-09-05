import datetime
from bson.objectid import ObjectId


class ContentMongoUtils(object):
    def __init__(self, mongo):
        self.mongo = mongo
        self.content_collection = 'content'

    def add_article(self, content):
        """ Insert article to the database.
         :param content: JSON object containing the content params
         :rtype: Boolean
        """
        self.mongo.db[self.content_collection] \
            .insert(content)
        return True

    def get_articles(self):
        """ Get articles from the database.
        :rtype: MongoDB Cursor with all the articles
        """
        articles = self.mongo.db[self.content_collection] \
            .find({'visible': True, 'published': True})

        return articles

    def get_paginated_articles(self, skips, limits):
        """ Get paginated articles from the database.
        :rtype: MongoDB Cursor with the queried articles
        """
        articles = self.mongo.db[self.content_collection] \
            .find({'visible': True, 'published': True}).sort([("_id",-1)]).limit(limits).skip(skips)
        return articles

    def get_authors_paginated_articles(self, author_id, skips, limits):
        """ Get paginated articles from the database for a specific author.
        :rtype: MongoDB Cursor with the queried articles
        """
        articles = self.mongo.db[self.content_collection] \
            .find({"user": author_id, 'visible': True, 'published': True}).skip(skips).limit(limits)
        return articles

    def get_single_article(self, slug):
        """ Get an article based on the title slug.
        :param slug: the slug version of the title
        :rtype: MongoDB cursor of the founded article.
        """
        articles = self.mongo.db[self.content_collection] \
            .find_one({"slug": slug})
        return articles

    def get_authors_articles(self, author_id):
        """ Get an article based on the author id.
        :param author_id: the id of the author who wrote the article
        :rtype: MongoDB cursor of the founded article.
        """
        articles = self.mongo.db[self.content_collection] \
            .find({"user": author_id})
        return articles

    def change_article_visibility(self, article_id, visible):
        """ Update the article to make it show/not show in the feed.
        :param article_id: the id of the article we want to change the visibility of
        :param visible: True or False
        :rtype: Boolean
        """
        if visible == 'True':
            update = self.mongo.db[self.content_collection] \
            .update({"_id": ObjectId(article_id)}, {'$set': {"visible": True}})
        elif visible == 'False':
            update = self.mongo.db[self.content_collection] \
            .update({"_id": ObjectId(article_id)}, {'$set': {"visible": False}})
        return update
