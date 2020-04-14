import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config():
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'bazinga'
	# DATABASE
	MONGODB_SETTINGS = {
		'db':   'isha',
		'host': 'localhost',
		'port': 27017
		#'username': ''
		#'password': ''
	}
	# E-MAIL
	MAIL_SERVER       = 'smtp.gmail.com'           #'localhost'
	MAIL_PORT         = 465                        #25
	MAIL_USE_TLS      = False                      #False
	MAIL_USE_SSL      = True                       #False
	MAIL_USERNAME     = 'seseikelle.bot@gmail.com' #None
	MAIL_PASSWORD     = 'D*`+snWfbYMUbhz!0CF2'     #None