import mongoengine as db
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from . import login_manager

@login_manager.user_loader
def load_user(user_id):
	return User.objects.with_id(user_id)

class User(UserMixin, db.Document):
	meta = {'collection': 'users'}
	email = db.EmailField(unique=True)
	confirmed = db.BooleanField(default=False)
	username = db.StringField(max_length=100, required=True, unique=True)
	pwhash = db.StringField(max_length=128, required=True)
	role_id = db.ReferenceField()

	def set_password(self, password):
		self.pwhash = generate_password_hash(password)

	def verify_password(self, password):
		return check_password_hash(self.pwhash, password)

	def generate_confirmation_token(self, expiration=3600):
		s = Serializer(current_app.config['SECRET_KEY'], expiration)
		return s.dumps({'confirm': self.get_id()}).decode('utf-8')

	def confirm(self, token):
		s = Serializer(current_app['SECRET_KEY'])
		try:
			data = s.loads(token.encode('utf-8'))
		except:
			return False
		if data.get('confirm') != self.get_id():
			return False
		self.confirmed = True
		self.save()
		return True

class Role(db.Document):
	meta = {'collection': 'roles'}
	name = db.StringField(max_length=100, unique=True)
	# default = db.BooleanField(default=False)
	# permissions = db.ListField()