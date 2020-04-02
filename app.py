from flask import Flask, request, render_template, redirect, session, url_for, flash
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, login_required, login_user, logout_user
from flask_mail import Mail
from flask_moment import Moment
from flask_mongoengine import MongoEngine
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User
from forms.user import UserForm
from forms.login import LoginForm
import secrets

app = Flask(__name__)
app.config.from_object(app.default_config)
app.config.from_object(secrets.Config)
bootstrap = Bootstrap(app)
moment = Moment(app)
mail = Mail(app)
db = MongoEngine(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
	return User.objects.get(id=user_id)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.objects.get(username=form.username.data)
		if user is not None and user.verify_password(form.password.data):
			login_user(user, form.remember_me.data)
			next = request.args.get('next')
			if next is None:
				next = url_for('index')
			return redirect(next)
	return render_template('login.html', form=form)

@app.route('/logout')
def logout():
	logout_user()
	flash('You have been logged out.')
	return redirect(url_for('index'))

@app.route('/secret')
@login_required
def secret():
	return 'top secret stuff lies here'

@app.route('/users')
def users():
	users = []
	for user in User.objects():
		users.append(user)
	return render_template('users.html', users=users)

@app.route('/users/new', methods=['GET', 'POST'])
def newuser():
	form = UserForm()
	if form.validate_on_submit():
		user = User()
		user.email = form.email.data
		user.username = form.username.data
		user.pwhash = generate_password_hash(form.password.data)
		user.save()
		flash('You can now log in.')
		return redirect(url_for('index'))
	return render_template('form.html', form=form)

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
	return render_template('500.html'), 500