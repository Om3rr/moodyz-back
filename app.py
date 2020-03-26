from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import settings

app = Flask(__name__, static_folder='build/static', template_folder="build")
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("JAWSDB_MARIA_URL")
db = SQLAlchemy(app)