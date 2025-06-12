from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_mail import Mail
from dotenv import load_dotenv
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os


app = Flask(__name__)
CORS(app)

load_dotenv()

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_CONN_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.getenv('GOOGLE_MAIL')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

app.secret_key = os.getenv('SECRET_KEY')

db = SQLAlchemy(app)
mail = Mail(app)
limiter = Limiter(get_remote_address, app=app)

import bibliothek.routes