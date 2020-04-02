import mongoengine as db
from flask_login import UserMixin
from werkzeug.security import check_password_hash

class User(UserMixin, db.Document):
	meta = {'collection': 'users'}
	email = db.EmailField()
	username = db.StringField(max_length=100, required=True)
	pwhash = db.StringField(max_length=128, required=True)
	role_id = db.ObjectIdField()

	def verify_password(self, password):
		return check_password_hash(self.pwhash, password)