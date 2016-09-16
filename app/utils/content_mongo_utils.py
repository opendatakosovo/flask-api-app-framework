import datetime
from bson.objectid import ObjectId
from bson.json_util import json

class ContentMongoUtils(object):
    def __init__(self, mongo):
        self.mongo = mongo
        self.content_collection = 'content'
        self.users_collection = 'users'

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

    def delete_article(self, id):
        """ Delete article from the database.
        :rtype: MongoDB Cursor with all the articles
        """
        articles = self.mongo.db[self.content_collection] \
            .remove({"_id":ObjectId(id)})

        return articles
    def search(self, text):
        """ Search articles from the database.
        :rtype: MongoDB Cursor with all the articles
        """
        articles = self.mongo.db[self.content_collection] \
            .find( { '$text': { '$search': text } } )

        return articles
    def get_paginated_articles(self, skips, limits):
        """ Get paginated articles from the database.
        :rtype: JSON with the queried articles
        """
        articles = self.mongo.db[self.content_collection] \
            .find({'visible': True, 'published': True}).sort([("_id",-1)]).limit(limits).skip(skips)

        articles_dump = list(articles)
        for article in articles_dump:

            avatar_url = self.mongo.db[self.users_collection] \
                .find_one({"username": article['username']})
            if avatar_url:
                article['avatar_url'] = avatar_url['avatar_url']
        return articles_dump

    def get_authors_paginated_articles(self, username, skips, limits):
        """ Get paginated articles from the database for a specific author.
        :rtype: MongoDB Cursor with the queried articles
        """
        articles = self.mongo.db[self.content_collection] \
            .find({"username": username, 'visible': True, 'published': True}).sort([("_id",-1)]).limit(limits).skip(skips)

        articles_dump = list(articles)
        for article in articles_dump:
            if article is not None:
                article['avatar_url'] = self.mongo.db[self.users_collection] \
                .find_one({"username": article['username']})['avatar_url']
        return articles_dump

    def get_single_article(self, slug):
        """ Get an article based on the title slug.
        :param slug: the slug version of the title
        :rtype: MongoDB cursor of the founded article.
        """
        articles = self.mongo.db[self.content_collection] \
            .find_one({"slug": slug})
        return articles

    def get_authors_articles(self, username):
        """ Get an article based on the author id.
        :param author_id: the id of the author who wrote the article
        :rtype: MongoDB cursor of the founded article.
        """
        articles = self.mongo.db[self.content_collection] \
            .find({"username": username}).sort([("_id",-1)])
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
