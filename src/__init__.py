import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# from config import DEFAULT_SQLALCHEMY_DATABASE_URL

app = Flask(__name__)
app.config.from_object(os.environ.get('APP_SETTINGS', 'config.Config'))
# app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
db = SQLAlchemy(app)

from . import views
