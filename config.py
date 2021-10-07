from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/shiv/Desktop/ARTIFY/database/artify.db'
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = '32da88840872ae1e55025005e9dd3bd4'

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = '587'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('ARTIFY_MAIL')
app.config['MAIL_PASSWORD'] = os.environ.get('ARTIFY_PASS')


db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
mail = Mail(app)