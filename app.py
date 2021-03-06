from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import settings

app = Flask(__name__, static_folder=None)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("JAWSDB_MARIA_URL")
db = SQLAlchemy(app)