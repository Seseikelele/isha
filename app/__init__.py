from flask import Flask
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_mongoengine import MongoEngine
import config

login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app():
	app = Flask(__name__)
	app.config.from_object(app.default_config)
	app.config.from_object(config.Config)
	bootstrap = Bootstrap(app)
	moment = Moment(app)
	mail = Mail(app)
	db = MongoEngine(app)
	login_manager.init_app(app)
	from .main import main as main_blueprint
	app.register_blueprint(main_blueprint)
	from .auth import auth as auth_blueprint
	app.register_blueprint(auth_blueprint, url_prefix='/auth')
	from .admin import admin as admin_blueprint
	app.register_blueprint(admin_blueprint, url_prefix='/admin')
	return app