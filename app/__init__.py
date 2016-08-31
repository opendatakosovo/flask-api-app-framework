from flask import Flask, g
import os
import ConfigParser
from logging.handlers import RotatingFileHandler
from flask.ext.pymongo import PyMongo
from app.utils.profile_mongo_utils import ProfileMongoUtils
from app.utils.user_mongo_utils import UserMongoUtils, Anonymous, User, Roles
from flask.ext.bcrypt import Bcrypt
from flask.ext.login import LoginManager
from flask.ext.security import Security, current_user
from bson.objectid import ObjectId

login_manager = LoginManager()


# Create MongoDB database object.
mongo = PyMongo()

bcrypt = Bcrypt()

security = Security()
# Initialize mongo access point
profile_mongo_utils = ProfileMongoUtils(mongo)
user_mongo_utils = UserMongoUtils(mongo)


def create_app():
    # Here we  create flask instance
    app = Flask(__name__)

    # Allow cross-domain access to API.
    #cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Load application configurations
    load_config(app)

    # Configure logging.
    configure_logging(app)

    # Configure login manager
    configure_login_manager(app)

    # Init modules
    init_modules(app)

    # Initialize the app to work with MongoDB
    mongo.init_app(app, config_prefix='MONGO')

    return app

def configure_login_manager(app):
    security.init_app(app)
    # Init Login Manager
    login_manager.init_app(app)

    login_manager.login_view='mod_user.login'

    login_manager.anonymous_user = Anonymous

    login_manager.user = User


@login_manager.user_loader
def user_loader(user_id):
    """Given *user_id*, return the associated User object.

    :param unicode user_id: user_id (email) user to retrieve
    """
    user = user_mongo_utils.get_user_by_id(ObjectId(user_id))

    return user


def load_config(app):
    ''' Reads the config file and loads configuration properties into the Flask app.
    :param app: The Flask app object.
    '''
    # Get the path to the application directory, that's where the config file resides.
    par_dir = os.path.join(__file__, os.pardir)
    par_dir_abs_path = os.path.abspath(par_dir)
    app_dir = os.path.dirname(par_dir_abs_path)

    # Read config file
    config = ConfigParser.RawConfigParser()
    config_filepath = app_dir + '/config.cfg'
    config.read(config_filepath)

    app.config['SERVER_PORT'] = config.get('Application', 'SERVER_PORT')
    app.config['MONGO_DBNAME'] = config.get('Mongo', 'DB_NAME')
    app.config['SECRET_KEY'] = config.get('Application', 'SECURITY_KEY')
    app.config['SECURITY_PASSWORD_SALT'] = config.get('Application', 'SECURITY_PASSWORD_SALT')
    app.config['SECURITY_REGISTREABLE'] = config.get('Application', 'SECURITY_REGISTREABLE')

    # db.connect(app.config['MONGO_DBNAME'], alias='default')
    # Logging path might be relative or starts from the root.
    # If it's relative then be sure to prepend the path with the application's root directory path.
    log_path = config.get('Logging', 'PATH')
    if log_path.startswith('/'):
        app.config['LOG_PATH'] = log_path
    else:
        app.config['LOG_PATH'] = app_dir + '/' + log_path

    app.config['LOG_LEVEL'] = config.get('Logging', 'LEVEL').upper()


def configure_logging(app):
    ''' Configure the app's logging.
     param app: The Flask app object
    '''

    log_path = app.config['LOG_PATH']
    log_level = app.config['LOG_LEVEL']

    # If path directory doesn't exist, create it.
    log_dir = os.path.dirname(log_path)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Create and register the log file handler.
    log_handler = RotatingFileHandler(log_path, maxBytes=250000, backupCount=5)
    log_handler.setLevel(log_level)
    app.logger.addHandler(log_handler)

    # First log informs where we are logging to.
    # Bit silly but serves  as a confirmation that logging works.
    app.logger.info('Logging to: %s', log_path)


def init_modules(app):

    # Import blueprint modules
    from app.mod_main.views import mod_main
    from app.mod_profile.views import mod_profile
    from app.mod_user.views import mod_user
    from app.mod_auth.views import mod_auth

    app.register_blueprint(mod_main)
    app.register_blueprint(mod_profile)
    app.register_blueprint(mod_user)
    app.register_blueprint(mod_auth)


