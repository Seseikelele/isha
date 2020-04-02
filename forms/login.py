import wtforms as wtf
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, Email

class LoginForm(FlaskForm):
	username = wtf.StringField('username', validators=[DataRequired()])
	password = wtf.PasswordField('password', validators=[DataRequired()])
	remember_me = wtf.BooleanField('keep me logged in')
	submit = wtf.SubmitField('log in')