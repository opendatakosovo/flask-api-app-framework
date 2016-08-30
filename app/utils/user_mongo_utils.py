from flask.ext.login import LoginManager, login_user, logout_user, \
     login_required, current_user
from flask.ext.security import UserMixin, RoleMixin
from flask.ext.login import AnonymousUserMixin

class UserMongoUtils(object):

    def __init__(self, mongo):
        self.mongo = mongo
        self.collection_name = 'users'

    def add_user(self, user):
        self.mongo.db[self.collection_name] \
            .insert(user)
        return True

    def get_user(self, email ):
        user_cursor = self.mongo.db[self.collection_name] \
            .find_one({"email":email})
        role = Roles( 'individual' , 'description')
        user_instance = User(unicode(user_cursor['_id']), user_cursor['active'], user_cursor['email'], user_cursor['password'] , role)
        return user_instance

    def get_user_by_id(self, id):
        user_cursor = self.mongo.db[self.collection_name] \
            .find_one({"_id": unicode(id)})
        user_instance = None
        if(user_cursor != None):
            user_instance = User(unicode(user_cursor['_id']), user_cursor['active'], user_cursor['email'],
                             user_cursor['password'], user_cursor['roles'])
        else:
            return None
        return user_instance


class User(UserMixin):
    def __init__(self,id, is_active, email, password, role):
        self.id = id
        self.is_active = is_active
        self.email = email
        self.password = password
        self.roles = [role]
        self.is_anonymous = False

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
    def __init__(self, name, description):
        self.name = name
        self.description = description

class Anonymous(UserMixin):
    def __init__(self):
        self.username = 'Guest'
        self.id = None
        self.roles = []
        self.is_authenticated = False

    def is_authenticated(self):
        return False

    def is_active(self):
        return False

    def get_id(self):
        return None
