from flask.ext.login import LoginManager, login_user, logout_user, \
     login_required, current_user
from flask.ext.security import UserMixin, RoleMixin
from flask.ext.login import AnonymousUserMixin
import datetime
from bson.objectid import ObjectId

class UserMongoUtils(object):

    def __init__(self, mongo):
        self.mongo = mongo
        self.users_collection = 'users'
        self.roles_collection = 'roles'

    def add_user(self, user):
        self.mongo.db[self.users_collection] \
                .insert(user)
        return True

    def get_role_id(self, name):
        role = self.mongo.db[self.roles_collection] \
            .find_one({"name":name})
        if role != None:
            return ObjectId(role['_id'])
        else:
            ## Add role
            self.mongo.db[self.roles_collection] \
            .insert({"name": name,'description': name})

            ## Get role
            role = self.mongo.db[self.roles_collection] \
            .find_one({"name":name})

            return ObjectId(role['_id'])

    def get_user(self, email ):
        user_cursor = self.mongo.db[self.users_collection] \
            .find_one({"email":email})
        if user_cursor == None:
            return None
        else:
            user_instance = User(unicode(user_cursor['_id']),user_cursor['name'], user_cursor['lastname'], user_cursor['active'], user_cursor['email'], user_cursor['password'] , user_cursor['roles'])
            return user_instance

    def get_user_by_id(self, id):
        user_cursor = self.mongo.db[self.users_collection] \
            .find_one({"_id": ObjectId(id)})
        user_instance = None
        if(user_cursor != None):
            user_instance = User(unicode(user_cursor['_id']), user_cursor['name'], user_cursor['lastname'], user_cursor['active'], user_cursor['email'],
                             user_cursor['password'], user_cursor['roles'])
        else:
            return None
        return user_instance


class User(UserMixin):
    def __init__(self,id,name,lastname, is_active, email, password, role):
        self.id = id
        self.name = name
        self.lastname = lastname
        self.is_active = is_active
        self.email = email
        self.password = password
        self.roles = [Roles( role , 'individual' , 'description')]
        self.is_anonymous = False
        self.confirmed_at = datetime.datetime.now()

    def is_active(self):
        return True

    def get_id(self):
        return unicode(self.id)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

class Roles(RoleMixin):
    def __init__(self, id, name, description):
        self.id = id
        self.name = name
        self.description = description

    def get_role(self):
        return this

class Anonymous(UserMixin):
    def __init__(self):
        self.username = 'Guest'
        self.id = None
        self.roles = []

    def is_authenticated(self):
        return False

    def is_active(self):
        return False

    def get_id(self):
        return None

    def is_anonymous(self):
        return True
