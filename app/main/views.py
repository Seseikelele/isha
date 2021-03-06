from flask import render_template
from flask_login import login_required
from . import main

@main.route('/')
def index():
	return render_template('index.html')

@main.route('/secret')
@login_required
def secret():
	return 'top secret stuff lies here'

@main.route('/users')
@login_required
def users():
	return render_template('users.html', users=User.objects())