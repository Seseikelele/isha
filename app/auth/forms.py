import wtforms as wtf
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, EqualTo
from wtforms import ValidationError
from ..models import User

class LoginForm(FlaskForm):
	username = wtf.StringField('username', validators=[DataRequired(), Length(1, 100)])
	password = wtf.PasswordField('password', validators=[DataRequired()])
	remember_me = wtf.BooleanField('keep me logged in')
	submit = wtf.SubmitField('log in')

class RegistrationForm(FlaskForm):
	username = wtf.StringField('username', validators=[DataRequired(), Length(1, 100)])
	password = wtf.PasswordField('password', validators=[DataRequired(), EqualTo('password2', 'passwords must match')])
	password2 = wtf.PasswordField('confirm password', validators=[DataRequired()])

	def validate_username(self, field):
		if User.objects.get(username=field.data) is not None:
			raise ValidationError('username already in use')