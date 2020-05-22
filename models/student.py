import os
import random, string

from app import db
from helpers.image_service import ProfilePicFetcher


def gen_auth():
    return "".join([random.choice(string.ascii_letters) for i in range(32)])


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    klass_id = db.Column(db.Integer, db.ForeignKey('klass.id', ondelete='CASCADE'),
                         nullable=False)
    name = db.Column(db.String(128))
    gender = db.Column(db.String(128))
    klass = db.relationship('Klass',
                            backref=db.backref('students', lazy=True))
    auth_token = db.Column(db.String(128), default=gen_auth)
    picture_url = db.Column(db.String(128))

    def to_dict(self, with_klass=False):
        d = dict(
            id=self.id,
            name=self.name,
            picture=self.picture_url,
            face_url=self.face_url,
            gender=self.gender,
            url="{}/login?pw={}".format(os.getenv("CURRENT_URL"), self.auth_token)
        )

        if with_klass:
            d.update(klass=self.klass.to_dict())
        return d


    @property
    def face_url(self):
        if not self.picture_url:
            return
        return ProfilePicFetcher.fetch(self.picture_url)
