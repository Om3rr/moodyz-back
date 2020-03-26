import random, string

from app import db


def gen_auth():
    return "".join([random.choice(string.ascii_letters) for i in range(32)])


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    klass_id = db.Column(db.Integer, db.ForeignKey('klass.id'),
                         nullable=False)
    name = db.Column(db.String(128))
    klass = db.relationship('Klass',
                            backref=db.backref('students', lazy=True))
    auth_token = db.Column(db.String(128), default=gen_auth)
    picture_url = db.Column(db.String(128))

    def to_dict(self):
        return dict(
            name=self.name,
            klass=self.klass.to_dict(),
            picture=self.picture_url
        )
