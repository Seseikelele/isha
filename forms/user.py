import wtforms as wtf
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, Email

class UserForm(FlaskForm):
	email = wtf.TextField('e-mail', validators=[Email()])
	username = wtf.TextField('username', validators=[DataRequired()])
	password = wtf.PasswordField('password', validators=[DataRequired(), Length(8, 100, 'password should be 8-100 characters long')])
	submit = wtf.SubmitField('register')