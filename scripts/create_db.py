from models import *
from app import db, app

with app.app_context():
    # your code here
    db.drop_all()
    db.create_all()
