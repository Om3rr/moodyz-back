from models import *
from sqlalchemy import MetaData
from app import db, app

with app.app_context():
    # your code here
    db.drop_all()
    db.create_all()
