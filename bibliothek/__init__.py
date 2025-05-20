from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv
import os

app = Flask(__name__)
CORS(app)

load_dotenv()

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_CONN_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

import bibliothek.routes