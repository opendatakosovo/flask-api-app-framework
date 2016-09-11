from bson.objectid import ObjectId
from app.mod_profile.mod_views.user import User
import re

class UserMongoUtils(object):

    def __init__(self, mongo):
        self.mongo = mongo
        self.users_collection = 'users'
        self.roles_collection = 'roles'

    def query(self, query):
        """ Make a query by only sending a JSON .
         :param query: JSON object containing the query params
         :rtype: Mongo Cursor
        """
        result = self.mongo.db[self.users_collection] \
            .find(query)
        return result

    def update(self, condition, update_json):
        """ Make a update by only sending a JSON .
         :param query: JSON object containing the update params
         :rtype: Mongo Cursor
        """
        result = self.mongo.db[self.users_collection] \
            .update(condition, {"$set":update_json})
        return result

    def add_user(self, user):
        """ Add user to the database.
         :param user: JSON object containing the user information
         :rtype: Boolean
        """
        user['location'] = ""
        user['mobile'] = ""
        user['telephone'] = ""
        user['about_me'] = ""
        user['role'] = "individual"
        user['avatar_url'] = ""
        user['username'] = re.sub("[!@#$%^&*()[]{};:,./<>?\|`~-=_+ ]", "", user['username']).replace(' ','').lower()
        self.mongo.db[self.users_collection] \
                .insert(user)
        return True

    def change_avatar(self, username, avatar_url):
        self.mongo.db[self.users_collection] \
            .update({"username":username},{"$set":{"avatar_url": avatar_url}})
        return True
    def get_role_id(self, name):
        role = self.mongo.db[self.roles_collection] \
            .find_one({"name":name})
        if role != None:
            return ObjectId(role['_id'])
        else:

            # Add role
            self.mongo.db[self.roles_collection] \
            .insert({"name": name,'description': name})

            # Get role
            role = self.mongo.db[self.roles_collection] \
            .find_one({"name":name})

            return ObjectId(role['_id'])

    def get_user(self, email):
        user_cursor = self.mongo.db[self.users_collection] \
            .find_one({"email":email})
        if user_cursor is None:
            return None
        else:
            user_instance = User(
                id=unicode(user_cursor['_id']),
                name=user_cursor['name'],
                lastname=user_cursor['lastname'],
                is_active=user_cursor['active'],
                email=user_cursor['email'],
                password=user_cursor['password'] ,
                roles = user_cursor['roles'],
                role=user_cursor['role'],
                username=user_cursor['username'],
                location= user_cursor['location'],
                telephone= user_cursor['telephone'],
                mobile = user_cursor['mobile'],
                about_me = user_cursor['about_me'],
                avatar_url = user_cursor['avatar_url']
            )
            return user_instance

    def get_users(self):
        users = self.mongo.db[self.users_collection] \
            .find()
        return users
    def get_user_by_username(self, username):
        user_cursor = self.mongo.db[self.users_collection] \
            .find_one({"username":username})
        if user_cursor is None:
            return None
        else:
           user_instance = User(
                id=unicode(user_cursor['_id']),
                name=user_cursor['name'],
                lastname=user_cursor['lastname'],
                is_active=user_cursor['active'],
                email=user_cursor['email'],
                password=user_cursor['password'] ,
                roles = user_cursor['roles'],
                role=user_cursor['role'],
                username=user_cursor['username'],
                location= user_cursor['location'],
                telephone= user_cursor['telephone'],
                mobile = user_cursor['mobile'],
                about_me = user_cursor['about_me'],
                avatar_url = user_cursor['avatar_url']
            )
           return user_instance

    def get_user_by_id(self, id):
        user_cursor = self.mongo.db[self.users_collection] \
            .find_one({"_id": ObjectId(id)})
        user_instance = None
        if user_cursor is not None:
            user_instance = User(
                id=unicode(user_cursor['_id']),
                name=user_cursor['name'],
                lastname=user_cursor['lastname'],
                is_active=user_cursor['active'],
                email=user_cursor['email'],
                password=user_cursor['password'] ,
                roles = user_cursor['roles'],
                role=user_cursor['role'],
                username=user_cursor['username'],
                location= user_cursor['location'],
                telephone= user_cursor['telephone'],
                mobile = user_cursor['mobile'],
                about_me = user_cursor['about_me'],
                avatar_url = user_cursor['avatar_url']
            )
        else:
            return None
        return user_instance

    def get_avatar_url(self, username):
        return self.mongo.db[self.users_collection] \
            .find_one({"username": username})['avatar_url']
