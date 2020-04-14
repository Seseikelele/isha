from flask import flash, render_template, request, redirect, url_for
from flask_login import login_user, logout_user, current_user, login_required
from . import auth
from ..models import User
from .forms import LoginForm, RegistrationForm
#TODO change password, reset password, change e-mail
@auth.before_app_request
def before_request():
	if current_user.is_authenticated and not current_user.confirmed and request.blueprint != 'auth' and request.endpoint != 'static':
		return redirect(url_for('auth.unconfirmed'))

@auth.route('/login', methods=['GET', 'POST'])
def login():
	def f(form):
		return render_template('auth/login.html', form=form)
	form = LoginForm()
	if not form.validate_on_submit():
		return f(form)
	user = None
	try:
		user = User.objects.get(username=form.username.data)
	except User.DoesNotExist:
		pass
	if user is None or not user.verify_password(form.password.data):
		flash('invalid username or password')
		return f(form)
	login_user(user, form.remember_me.data)
	next = request.args.get('next')
	if next is None or not next.startswith('/'):
		next = url_for('main.index')
	return redirect(next)

@auth.route('/logout')
def logout():
	logout_user()
	flash('you have been logged out')
	return redirect(url_for('main.index'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	if not form.validate_on_submit():
		return render_template('auth/register.html', form=form)
	user = User()
	user.username = form.username.data
	user.set_password(form.password.data)
	user.save()
	#token = user.generate_confirmation_token()
	#send_email(user.email, 'Activate Your Account', 'auth/email/confirm', user=user, token=token)
	flash('you can now log in')#a confirmation e-mail has been sent
	return redirect(url_for('main.index'))
	# return redirect(url_for('auth.login'))

@auth.route('/confirm/<token>')
@login_required
def confirm(token):
	if current_user.confirmed:
		return redirect(url_for('main.index'))
	if current_user.confirm(token):
		flash('you have confirmed your account')
	else:
		flash('the link is invalid or has expired')
	return redirect(url_for('main.index'))

@auth.route('/unconfirmed')
def unconfirmed():
	if current_user.is_anonymous or current_user.confirmed:
		return redirect(url_for('main.index'))
	return render_template('auth/unconfirmed.html')

@auth.route('/confirm')
@login_required
def resend_confirmation():
	token = current_user.generate_confirmation_token()
	#send_email(user.email, 'Activate Your Account', 'auth/email/confirm', user=user, token=token)
	flash('a confirmation e-mail has been sent')
	return redirect(url_for('main.index'))