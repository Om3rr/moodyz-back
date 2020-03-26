from app import db


class Klass(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(16))
    slug = db.Column(db.String(16), index=True)